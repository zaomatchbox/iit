from typing import List

from ..schema.attr import Attr
from ..schema.dim import Dimension
from ..schema.hier import Hierarchy
from ..schema.level import Level


class Parser:

    def __init__(self) -> None:
        self._pos = 0
        self._state = []
        self._is_tag = False
        self._is_value = False
        self._current_token = []
        self._current_tag = []
        self._line_no = 1
        self._content_start = False
        self._objects = []
        self._model = []
        self._scope = {
            'dim': None,
            'levels': {},
        }

    def feed(self, src: str) -> None:
        for ch in src:
            self._feed_char(ch)

    def _feed_char(self, ch: str) -> str:
        if ch == '{':
            if self._content_start:
                if self._is_tag:
                    raise SyntaxError(
                        f'Line {self._line_no}: Unexpected token "{ch}"')
                self._is_tag = True
            else:
                self._content_start = True
        elif ch == ':':
            if self._is_tag or self._is_value:
                raise SyntaxError(
                    f'Line {self._line_no}: Unexpected token "{ch}"')
            self._is_value = True
        elif ch == '}':
            if self._is_tag:
                self._is_tag = False
            else:
                self._content_start = False
                self.save_token()
        elif ch == ' ':
            if self._is_tag:
                raise SyntaxError(
                    f'Line {self._line_no}: Tags cannot contain space')
            if self._is_value:
                self._current_token.append(ch)
        elif ch == '\n':
            if self._is_tag:
                raise SyntaxError(
                    f'Line {self._line_no}: Unexpected newline symbol inside tag')
            self.save_token()
            self._line_no += 1
            self._is_value = False
        else:
            if self._is_tag:
                self._current_tag.append(ch)
                return
            if self._is_value:
                self._current_token.append(ch)
                return
            raise SyntaxError(
                f'Line {self._line_no}: Unexpected token "{ch}"')

    @property
    def current_token(self) -> str:
        return ''.join(self._current_token).strip()

    @property
    def current_tag(self) -> str:
        return ''.join(self._current_tag)

    def save_token(self) -> None:
        tag = self.current_tag
        token = self.current_token
        if tag == 'Dim':
            self._state.append({
                'kind': 'dim',
                'name': token,
            })
        elif tag == 'Level':
            self._state.append({
                'kind': 'level',
                'name': token,
            })
        elif tag == 'Attr':
            self._state.append({
                'kind': 'attr',
                'name': token,
            })
        elif tag == 'Attr.Type':
            if self._state[-1]['kind'] == 'attr':
                self._state[-1]['type'] = token
            else:
                raise ValueError()
        elif tag == 'Hier':
            self._state.append({
                'kind': 'hier',
                'name': token,
            })
        elif tag == 'Hier.Levels':
            if self._state[-1]['kind'] == 'hier':
                self._state[-1]['levels'] = token
            else:
                raise ValueError()
        elif tag == 'Dim.Info':
            if self._state[-1]['kind'] == 'dim':
                self._state[-1]['info'] = token
            else:
                raise ValueError()
        elif tag == 'Level.Info':
            if self._state[-1]['kind'] == 'level':
                self._state[-1]['info'] = token
            else:
                raise ValueError()
        elif tag == 'Hier.Info':
            if self._state[-1]['kind'] == 'hier':
                self._state[-1]['info'] = token
            else:
                raise ValueError()
        elif tag == 'Attr.Info':
            if self._state[-1]['kind'] == 'attr':
                self._state[-1]['info'] = token
            else:
                raise ValueError()

        self.try_record_node()
        self.reset_current_state()

    def reset_current_state(self) -> None:
        self._current_tag = []
        self._current_token = []

    def try_record_node(self) -> None:
        if len(self._state) == 0:
            return
        node = self._state[-1]
        if self._state[-1].get('is_complete', False):
            if 'info' in node:
                self._objects[-1].info = node['info']
            return
        kind = node['kind']
        if kind == 'dim':
            if 'name' in node:
                self._state[-1]['is_complete'] = True
                dim = Dimension(name=node['name'])
                self._scope['dim'] = dim
                self._objects.append(dim)
        elif kind == 'level':
            if 'name' in node:
                self._state[-1]['is_complete'] = True
                level = Level(name=node['name'])
                self._scope['levels'][level.name] = level
                self._objects.append(level)
        elif kind == 'attr':
            if 'name' in node and 'type' in node:
                self._state[-1]['is_complete'] = True
                attr = Attr(name=node['name'], type=node['type'])
                self._objects.append(attr)
        elif kind == 'hier':
            if 'name' in node and 'levels' in node:
                self._state[-1]['is_complete'] = True
                hier = Hierarchy(name=node['name'])
                levels = [l.strip() for l in node['levels'].split(',')]
                hier.add_levels([self._scope['levels'][level]
                                 for level in levels])
                self._objects.append(hier)

    @property
    def model(self) -> List[Dimension]:
        dims = []
        for i in self._objects:
            if isinstance(i, Dimension):
                dims.append(i)
            elif isinstance(i, Level):
                dims[-1].add_level(i)
            elif isinstance(i, Attr):
                dims[-1].levels[-1].add_attr(i)
            elif isinstance(i, Hierarchy):
                dims[-1].add_hier(i)
        return dims
