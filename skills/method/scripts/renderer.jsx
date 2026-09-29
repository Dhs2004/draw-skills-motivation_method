import {convertToExcalidrawElements, exportToSvg, exportToBlob} from '@excalidraw/excalidraw';
window.run = async () => {
  const {source, scale, padding} = await (await fetch('/payload.json')).json();
  const canonical = source.type === 'excalidraw';
  const warnings = [];
  let elements;
  if (canonical) {
    // Never remeasure, reconvert, reposition or otherwise mutate a saved scene.
    elements = source.elements.filter(e => !e.isDeleted);
  } else {
    const names = {1:'Virgil',2:'Helvetica',3:'Cascadia',5:'Excalifont',6:'Nunito',7:'Lilita One',8:'Comic Shanns',9:'Liberation Sans'};
    const family = id => id === 5 ? '"Excalifont", "Xiaolai", "Segoe UI Emoji"' : `"${names[id]}"`;
    const ctx = document.createElement('canvas').getContext('2d');
    // Let Excalidraw select and embed the actual font subsets for the text.
    const draft = convertToExcalidrawElements(structuredClone(source.elements), {regenerateIds:false});
    const fontSvg = await exportToSvg({elements:draft, appState:{exportBackground:false}, files:source.files||{}});
    for (const style of fontSvg.querySelectorAll('style')) {
      const css = document.createElement('style'); css.textContent=style.textContent; document.head.appendChild(css);
    }
    for (const e of source.elements.filter(e=>e.type==='text')) {
      if (!names[e.fontFamily]) throw new Error(`Unsupported font family ${e.fontFamily}`);
      await document.fonts.load(`${e.fontSize}px ${family(e.fontFamily)}`,e.text);
    }
    await document.fonts.ready;
    for (const e of source.elements) if (e.type === 'text') {
      ctx.font = `${e.fontSize}px ${family(e.fontFamily)}`;
      const width = Math.max(...e.text.split('\n').map(t => ctx.measureText(t).width));
      if (e.layoutWidth && width > e.layoutWidth + 0.5)
        throw new Error(`Text exceeds layoutWidth; reflow rather than shrink silently: ${e.text}`);
      if (e.textAlign === 'center') e.x += ((e.layoutWidth || e.width) - width) / 2;
      if (e.textAlign === 'right') e.x += (e.layoutWidth || e.width) - width;
      e.width = width; e.height = e.text.split('\n').length * e.fontSize * (e.lineHeight || 1.3);
      delete e.layoutWidth;
    }
    elements = convertToExcalidrawElements(source.elements, {regenerateIds:false});
    // Conversion can recenter text. Keep explicitly measured positions.
    const originals = new Map(source.elements.map(e=>[e.id,e]));
    for (const e of elements) if (e.type==='text') {const o=originals.get(e.id);e.x=o.x;e.y=o.y;}
  }
  const ids = new Set();
  for (const e of elements) {
    if (ids.has(e.id)) throw new Error(`Duplicate element ID: ${e.id}`); ids.add(e.id);
    for (const k of ['x','y','width','height']) if (!Number.isFinite(e[k])) throw new Error(`Invalid ${e.id}.${k}`);
    if (e.type==='image' && !source.files?.[e.fileId]) throw new Error(`Missing image: ${e.fileId}`);
    if (e.type==='text' && e.fontSize < 14) warnings.push(`Small text: ${e.text}`);
  }
  // Report image/text intersections; image-image overlap can be intentional.
  for (const t of elements.filter(e=>e.type==='text')) for (const i of elements.filter(e=>e.type==='image')) {
    if (t.x < i.x+i.width && t.x+t.width > i.x && t.y < i.y+i.height && t.y+t.height > i.y)
      warnings.push(`Review image/text overlap: ${i.id} / ${t.text}`);
  }
  const state = {...source.appState, exportBackground:true, exportWithDarkMode:false,
                 viewBackgroundColor:source.appState?.viewBackgroundColor || '#ffffff', exportEmbedScene:false};
  window.scene = canonical ? source : {type:'excalidraw',version:2,source:'https://excalidraw.com',elements,
                                       appState:{viewBackgroundColor:state.viewBackgroundColor,gridSize:null},files:source.files||{}};
  const svg = await exportToSvg({elements,appState:state,files:source.files||{},exportPadding:padding});
  document.body.replaceChildren(svg); await document.fonts.ready;
  window.svgText = new XMLSerializer().serializeToString(svg);
  const blob = await exportToBlob({elements,appState:state,files:source.files||{},exportPadding:padding,
                                  mimeType:'image/png',getDimensions:(w,h)=>({width:w*scale,height:h*scale,scale})});
  window.png = await new Promise(resolve=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.readAsDataURL(blob)});
  return {width:parseFloat(svg.getAttribute('width')),height:parseFloat(svg.getAttribute('height')),
          elements:elements.length,images:elements.filter(e=>e.type==='image').length,warnings};
};
