# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
# Created 2019-03-06
from typing import TYPE_CHECKING, Iterable, Sequence, Tuple, Union, List, Dict
import array
import copy
from itertools import chain

from contextlib import contextmanager
from ezdxf.lldxf.attributes import DXFAttr, DXFAttributes, DefSubclass
from ezdxf.lldxf.const import SUBCLASS_MARKER, DXF2000, DXFValueError, DXFStructureError
from ezdxf.lldxf.packedtags import VertexArray, TagArray, TagList
from ezdxf.tools import take2
from .dxfentity import base_class, SubclassProcessor
from .dxfgfx import DXFGraphic, acdb_entity

from .factory import register_entity

if TYPE_CHECKING:
    from ezdxf.eztypes import TagWriter, DXFNamespace, Drawing, Vertex, Tags

__all__ = ['Mesh', 'MeshData']

acdb_mesh = DefSubclass('AcDbSubDMesh', {
    'version': DXFAttr(71, default=2),
    'blend_crease': DXFAttr(72, default=0),  # 0 = off, 1 = on
    'subdivision_levels': DXFAttr(91, default=0),  # int >= 0, 0 is no smoothing
    # 92: Vertex count of level 0
    # 10: Vertex position, multiple entries
    # 93: Size of face list of level 0
    # 90: Face list item, >=3 possible
    #     90: length of face list
    #     90: 1st vertex index
    #     90: 2nd vertex index ...
    # 94: Edge count of level 0
    #     90: Vertex index of 1st edge
    #     90: Vertex index of 2nd edge
    # 95: Edge crease count of level 0
    #     95 same as 94, or how is the 'edge create value' associated to edge index
    # 140: Edge crease value
    #
    # Overriding properties: how does this work?
    # 90: Count of sub-entity which property has been overridden
    # 91: Sub-entity marker
    # 92: Count of property was overridden
    # 90: Property type
    #     0 = Color
    #     1 = Material
    #     2 = Transparency
    #     3 = Material mapper
})


class EdgeArray(TagArray):
    DTYPE = 'L'

    def __len__(self) -> int:
        return len(self.values) // 2

    def __iter__(self) -> Iterable[Tuple[int, int]]:
        for edge in take2(self.values):
            yield edge

    def set_data(self, edges: Iterable[Tuple[int, int]]) -> None:
        self.values = array.array(self.DTYPE, chain.from_iterable(edges))

    def export_dxf(self, tagwriter: 'TagWriter'):
        # count = count of edges not tags!
        tagwriter.write_tag2(94, len(self.values) // 2)
        for index in self.values:
            tagwriter.write_tag2(90, index)


class FaceList(TagList):
    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self) -> Iterable[array.array]:
        return iter(self.values)

    def export_dxf(self, tagwriter: 'TagWriter'):
        # count = count of tags not faces!
        tagwriter.write_tag2(93, self.tag_count())
        for face in self.values:
            tagwriter.write_tag2(90, len(face))
            for index in face:
                tagwriter.write_tag2(90, index)

    def tag_count(self) -> int:
        return len(self.values) + sum(len(f) for f in self.values)

    def set_data(self, faces: Iterable[Sequence[int]]) -> None:
        _faces = []
        for face in faces:
            _faces.append(face_to_array(face))
        self.values = _faces


def face_to_array(face: Sequence[int]) -> array.array:
    max_index = max(face)
    if max_index < 256:
        dtype = 'B'
    elif max_index < 65536:
        dtype = 'I'
    else:
        dtype = 'L'
    return array.array(dtype, face)


def create_vertex_array(tags: 'Tags', start_index: int) -> 'VertexArray':
    vertex_tags = tags.collect_consecutive_tags(codes=(10,), start=start_index)
    return VertexArray(data=chain.from_iterable(t.value for t in vertex_tags))


def create_face_list(tags: 'Tags', start_index: int) -> 'FaceList':
    faces = FaceList()
    faces_list = faces.values
    face = []
    counter = 0
    for tag in tags.collect_consecutive_tags(codes=(90,), start=start_index):
        if not counter:
            # leading counter tag
            counter = tag.value
            if face:
                # group code 90 = 32 bit integer
                faces_list.append(face_to_array(face))
                face = []
        else:
            # followed by count face tags
            counter -= 1
            face.append(tag.value)

    # add last face
    if face:
        # group code 90 = 32 bit integer
        faces_list.append(face_to_array(face))

    return faces


def create_edge_array(tags: 'Tags', start_index: int) -> 'EdgeArray':
    return EdgeArray(data=collect_values(tags, start_index, code=90))  # int values


def collect_values(tags: 'Tags', start_index: int, code: int) -> Iterable[Union[float, int]]:
    values = tags.collect_consecutive_tags(codes=(code,), start=start_index)
    return (t.value for t in values)


def create_crease_array(tags: 'Tags', start_index: int) -> 'array.array':
    return array.array('f', collect_values(tags, start_index, code=140))  # float values


COUNT_ERROR_MSG = "'MESH (#{}) without {} count.'"


@register_entity
class Mesh(DXFGraphic):
    """ DXF MESH entity """
    DXFTYPE = 'MESH'
    DXFATTRIBS = DXFAttributes(base_class, acdb_entity, acdb_mesh)
    MIN_DXF_VERSION_FOR_EXPORT = DXF2000

    def __init__(self, doc: 'Drawing' = None):
        super().__init__(doc)
        self._vertices = VertexArray()  # vertices stored as array.array('d')
        self._faces = FaceList()  # face lists data
        self._edges = EdgeArray()  # edge indices stored as array.array('L')
        self._creases = array.array('f')  # creases stored as array.array('f')

    def _copy_data(self, entity: 'Mesh') -> None:
        """ Copy data: vertices, faces, edges, creases. """
        entity._vertices = copy.deepcopy(self._vertices)
        entity._faces = copy.deepcopy(self._faces)
        entity._edges = copy.deepcopy(self._edges)
        entity._creases = copy.deepcopy(self._creases)

    def load_dxf_attribs(self, processor: SubclassProcessor = None) -> 'DXFNamespace':
        dxf = super().load_dxf_attribs(processor)
        if processor:
            tags = processor.find_subclass(acdb_mesh.name)
            # load spline data (fit points, control points, weights, knots) and remove their tags from subclass
            self.load_mesh_data(tags, dxf.handle)
            # load remaining data into name space
            tags = processor.load_dxfattribs_into_namespace(dxf, acdb_mesh)
            if len(tags):  # override data
                processor.log_unprocessed_tags(tags, subclass=acdb_mesh.name)
        return dxf

    def load_mesh_data(self, mesh_tags: 'Tags', handle: str) -> None:
        def process_vertices():
            try:
                vertex_count_index = mesh_tags.tag_index(92)
            except DXFValueError:
                raise DXFStructureError(COUNT_ERROR_MSG.format(handle, 'vertex'))
            vertices = create_vertex_array(mesh_tags, vertex_count_index + 1)
            # remove vertex count tag and all vertex tags
            end_index = vertex_count_index + 1 + len(vertices)
            del mesh_tags[vertex_count_index:end_index]
            return vertices

        def process_faces():
            try:
                face_count_index = mesh_tags.tag_index(93)
            except DXFValueError:
                raise DXFStructureError(COUNT_ERROR_MSG.format(handle, 'face'))
            else:
                # remove face count tag and all face tags
                faces = create_face_list(mesh_tags, face_count_index + 1)
                end_index = face_count_index + 1 + faces.tag_count()
                del mesh_tags[face_count_index:end_index]
                return faces

        def process_edges():
            try:
                edge_count_index = mesh_tags.tag_index(94)
            except DXFValueError:
                raise DXFStructureError(COUNT_ERROR_MSG.format(handle, 'edge'))
            else:
                edges = create_edge_array(mesh_tags, edge_count_index + 1)
                # remove edge count tag and all edge tags
                end_index = edge_count_index + 1 + len(edges.values)
                del mesh_tags[edge_count_index:end_index]
                return edges

        def process_creases():
            try:
                crease_count_index = mesh_tags.tag_index(95)
            except DXFValueError:
                raise DXFStructureError(COUNT_ERROR_MSG.format(handle, 'crease'))
            else:
                creases = create_crease_array(mesh_tags, crease_count_index + 1)
                # remove crease count tag and all crease tags
                end_index = crease_count_index + 1 + len(creases)
                del mesh_tags[crease_count_index:end_index]
                return creases

        self._vertices = process_vertices()
        self._faces = process_faces()
        self._edges = process_edges()
        self._creases = process_creases()

    def export_entity(self, tagwriter: 'TagWriter') -> None:
        """ Export entity specific data as DXF tags. """
        # base class export is done by parent class
        super().export_entity(tagwriter)
        # AcDbEntity export is done by parent class
        tagwriter.write_tag2(SUBCLASS_MARKER, acdb_mesh.name)
        self.dxf.export_dxf_attribs(tagwriter, ['version', 'blend_crease', 'subdivision_levels'])
        self.export_mesh_data(tagwriter)
        self.export_override_data(tagwriter)

    def export_mesh_data(self, tagwriter: 'TagWriter'):
        tagwriter.write_tag2(92, len(self.vertices))
        self._vertices.export_dxf(tagwriter, code=10)
        self._faces.export_dxf(tagwriter)
        self._edges.export_dxf(tagwriter)

        tagwriter.write_tag2(95, len(self.creases))
        for crease_value in self.creases:
            tagwriter.write_tag2(140, crease_value)

    def export_override_data(self, tagwriter: 'TagWriter'):
        tagwriter.write_tag2(90, 0)

    @property
    def creases(self) -> 'array.array':  # group code 40
        """ Creases as :class:`array.array`. (read/write)"""
        return self._creases

    @creases.setter
    def creases(self, values: Iterable[float]) -> None:
        self._creases = array.array('f', values)

    @property
    def vertices(self):
        """ Vertices as list like :class:`~ezdxf.lldxf.packedtags.VertexArray`. (read/write)"""
        return self._vertices

    @vertices.setter
    def vertices(self, points: Iterable['Vertex']) -> None:
        self._vertices = VertexArray(chain.from_iterable(points))

    @property
    def edges(self):
        """ Edges as list like :class:`~ezdxf.lldxf.packedtags.TagArray`. (read/write)"""
        return self._edges

    @edges.setter
    def edges(self, edges: Iterable[Tuple[int, int]]) -> None:
        self._edges.set_data(edges)

    @property
    def faces(self):
        """ Faces as list like :class:`~ezdxf.lldxf.packedtags.TagList`. (read/write)"""
        return self._faces

    @faces.setter
    def faces(self, faces: Iterable[Sequence[int]]) -> None:
        self._faces.set_data(faces)

    def get_data(self) -> 'MeshData':
        return MeshData(self)

    def set_data(self, data: 'MeshData') -> None:
        self.vertices = data.vertices
        self._faces.set_data(data.faces)
        self._edges.set_data(data.edges)
        self.creases = data.edge_crease_values

    @contextmanager
    def edit_data(self) -> 'MeshData':
        """ Context manager various mesh data, returns :class:`MeshData`.

        Despite that vertices, edge and faces since `ezdxf` v0.8.9 are accessible as packed data types, the usage
        of :class:`MeshData` by context manager :meth:`edit_data` is still recommended.

        """
        data = self.get_data()
        yield data
        self.set_data(data)


class MeshData:
    def __init__(self, mesh):
        self.vertices = list(mesh.vertices)  # type: List[Tuple[float, float, float]]
        self.faces = list(mesh.faces)  # type: List[array.array]
        self.edges = list(mesh.edges)  # type: List[Tuple[int, int]]
        self.edge_crease_values = mesh.creases  # type: array.array

    def add_face(self, vertices: Iterable[Sequence[float]]) -> Sequence[int]:
        """ Add a face by coordinates, vertices is a list of ``(x, y, z)`` tuples. """
        return self.add_entity(vertices, self.faces)

    def add_edge(self, vertices: Sequence[Sequence[float]]) -> Sequence[int]:
        """ Add an edge by coordinates, vertices is a list of two ``(x, y, z)`` tuples. """
        if len(vertices) != 2:
            raise DXFValueError("Parameter vertices has to be a list/tuple of 2 vertices [(x1, y1, z1), (x2, y2, z2)].")
        return self.add_entity(vertices, self.edges)

    def add_entity(self, vertices: Iterable[Sequence[float]], entity_list: List) -> Sequence[int]:
        indices = [self.add_vertex(vertex) for vertex in vertices]
        entity_list.append(indices)
        return indices

    def add_vertex(self, vertex: Sequence[float]) -> int:
        if len(vertex) != 3:
            raise DXFValueError('Parameter vertex has to be a 3-tuple (x, y, z).')
        index = len(self.vertices)
        self.vertices.append(vertex)
        return index

    def optimize(self, precision: int = 6):
        """
        Tries to reduce vertex count by merging near vertices. `precision` defines the decimal places for coordinate
        be equal to merge two vertices.

        """
        def remove_doublette_vertices() -> Dict[int, int]:
            def prepare_vertices() -> Iterable[Tuple[float, float, float]]:
                for index, vertex in enumerate(self.vertices):
                    x, y, z = vertex
                    yield round(x, precision), round(y, precision), round(z, precision), index

            sorted_vertex_list = list(sorted(prepare_vertices()))
            original_vertices = self.vertices
            self.vertices = []
            index_map = {}  # type: Dict[int, int]
            cmp_vertex = None
            index = 0
            while len(sorted_vertex_list):
                vertex_entry = sorted_vertex_list.pop()
                original_index = vertex_entry[3]
                vertex = original_vertices[original_index]
                if vertex != cmp_vertex:  # this is not a doublette
                    index = len(self.vertices)
                    self.vertices.append(vertex)
                    index_map[original_index] = index
                    cmp_vertex = vertex
                else:  # it is a doublette
                    index_map[original_index] = index
            return index_map

        def remap_faces() -> None:
            self.faces = remap_indices(self.faces)

        def remap_edges() -> None:
            self.edges = remap_indices(self.edges)

        def remap_indices(entity_list: Sequence[Sequence[int]]) -> List[Tuple]:
            mapped_indices = []  # type: List[Tuple]
            for entity in entity_list:
                index_list = [index_map[index] for index in entity]
                mapped_indices.append(tuple(index_list))
            return mapped_indices

        index_map = remove_doublette_vertices()
        remap_faces()
        remap_edges()
