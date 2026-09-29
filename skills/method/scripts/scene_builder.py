"""Create a new editable scene skeleton; do not use to regenerate user-edited scenes."""
import base64
import hashlib
import json
import mimetypes
from pathlib import Path


class Scene:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.elements, self.files = [], {}
        self.box(0, 0, width, height, stroke='#ffffff', stroke_width=0, roughness=0)['locked'] = True

    def element(self, kind, x, y, width, height, **opts):
        n = len(self.elements)
        e = dict(id=f'figure-{n:04d}', type=kind, x=x, y=y, width=width, height=height,
                 angle=0, strokeColor='#252525', backgroundColor='transparent', fillStyle='solid',
                 strokeWidth=1.5, roughness=0.85, opacity=100, seed=7341+n*53, groupIds=[], locked=False)
        e.update(opts)
        self.elements.append(e)
        return e

    def box(self, x, y, w, h, fill='#ffffff', stroke='#252525', stroke_width=1.7,
            roughness=0.85, hachure=False):
        return self.element('rectangle', x, y, w, h, backgroundColor=fill, strokeColor=stroke,
                            strokeWidth=1 if hachure else stroke_width, roughness=1 if hachure else roughness,
                            fillStyle='hachure' if hachure else 'solid', roundness={'type': 3})

    def text(self, x, y, value, size=17, width=None, align='left', color='#303030', font=8):
        """width is the layout box; renderer measures text and centers within it if requested."""
        return self.element('text', x, y, width or 100, size*1.3, text=value,
                            fontSize=size, fontFamily=font, textAlign=align, verticalAlign='top',
                            lineHeight=1.3, autoResize=True, strokeColor=color, layoutWidth=width)

    def line(self, x, y, points, color='#252525', arrow=False, width=1.5):
        # The first point is the element anchor; callers should start with [0, 0].
        if points[0] != [0, 0]:
            raise ValueError('First point must be [0, 0]')
        e = self.element('arrow' if arrow else 'line', x, y,
                         max(p[0] for p in points)-min(p[0] for p in points),
                         max(p[1] for p in points)-min(p[1] for p in points),
                         points=points, strokeColor='#df3b3b' if arrow else color,
                         strokeWidth=2.3 if arrow else width, roughness=1, roundness={'type': 2})
        if arrow:
            e.update(startArrowhead=None, endArrowhead='arrow')
        return e

    def icon(self, path, x, y, w, h=None):
        """Use square PNG assets or explicitly supply proportional height."""
        path = Path(path)
        data = path.read_bytes()
        key = hashlib.sha256(data).hexdigest()[:24]
        mime = mimetypes.guess_type(path.name)[0] or 'image/png'
        self.files[key] = dict(id=key, mimeType=mime, created=1,
                               dataURL=f'data:{mime};base64,'+base64.b64encode(data).decode())
        return self.element('image', x, y, w, h if h is not None else w,
                            fileId=key, scale=[1, 1], status='saved')

    def save(self, path):
        Path(path).write_text(json.dumps(dict(width=self.width, height=self.height,
                                             elements=self.elements, files=self.files), ensure_ascii=False))
