#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import http from 'node:http';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import crypto from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url));
const args={};
for(let i=2;i<process.argv.length;i+=2){
  const k=process.argv[i];if(!['--input','--out-prefix','--runtime','--scale','--padding','--browser'].includes(k)||!process.argv[i+1])throw new Error('Usage: node export_scene.mjs --input scene.json --out-prefix /output/figure [--runtime DIR] [--scale 3] [--padding 8] [--browser PATH]');
  args[k.slice(2)]=process.argv[i+1];
}
if(!args.input||!args['out-prefix'])throw new Error('--input and --out-prefix are required');
const input=path.resolve(args.input),prefix=path.resolve(args['out-prefix']);
const runtime=path.resolve(args.runtime||path.join(here,'runtime'));
const scale=Number(args.scale||3),padding=Number(args.padding??8);
if(!Number.isInteger(scale)||scale<1||scale>8||!Number.isFinite(padding)||padding<0)throw new Error('Invalid scale/padding');
const require=createRequire(path.join(runtime,'package.json'));
const {build}=require('esbuild');const {chromium}=require('playwright');
let packageRoot=path.dirname(require.resolve('@excalidraw/excalidraw'));
while(true){try{if(JSON.parse(await fs.readFile(path.join(packageRoot,'package.json'),'utf8')).name==='@excalidraw/excalidraw')break;}catch{}
  const up=path.dirname(packageRoot);if(up===packageRoot)throw new Error('Cannot find Excalidraw package');packageRoot=up;
}
const fontsRoot=path.join(packageRoot,'dist','prod','fonts');
const original=await fs.readFile(input);const source=JSON.parse(original);
if(!Array.isArray(source.elements))throw new Error('Input needs elements[]');
if(source.type!=='excalidraw'&&input===prefix+'.excalidraw')throw new Error('Do not overwrite a skeleton input; choose a distinct output prefix');
const temp=await fs.mkdtemp(path.join(os.tmpdir(),'motivation-export-'));
let server,browser;
function pngDpi(buffer,dpi=300){
  const data=Buffer.alloc(9);data.writeUInt32BE(Math.round(dpi/0.0254),0);data.writeUInt32BE(Math.round(dpi/0.0254),4);data[8]=1;
  const type=Buffer.from('pHYs');let crc=0xffffffff;
  for(const v of Buffer.concat([type,data])){crc^=v;for(let i=0;i<8;i++)crc=(crc>>>1)^((crc&1)?0xedb88320:0);}
  const chunk=Buffer.alloc(21);chunk.writeUInt32BE(9);type.copy(chunk,4);data.copy(chunk,8);chunk.writeUInt32BE((crc^0xffffffff)>>>0,17);
  const parts=[buffer.subarray(0,8)];let pos=8;
  while(pos<buffer.length){const len=buffer.readUInt32BE(pos),name=buffer.toString('ascii',pos+4,pos+8);if(name!=='pHYs')parts.push(buffer.subarray(pos,pos+len+12));if(name==='IHDR')parts.push(chunk);pos+=len+12;}
  return Buffer.concat(parts);
}
try{
  await build({stdin:{contents:await fs.readFile(path.join(here,'renderer.jsx'),'utf8'),resolveDir:runtime,loader:'jsx'},
    bundle:true,outfile:path.join(temp,'bundle.js'),define:{'process.env.NODE_ENV':'"production"'},loader:{'.woff2':'file'},logLevel:'error'});
  await fs.writeFile(path.join(temp,'payload.json'),JSON.stringify({source,scale,padding}));
  await fs.writeFile(path.join(temp,'index.html'),'<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:white}svg{display:block}</style><script>window.EXCALIDRAW_ASSET_PATH="/";</script></head><body><script src="/bundle.js"></script></body></html>');
  server=http.createServer(async(req,res)=>{try{
    const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const root=pathname.startsWith('/fonts/')?fontsRoot:temp;
    const relative=pathname.startsWith('/fonts/')?pathname.slice(7):pathname==='/'?'index.html':pathname.slice(1);
    const target=path.resolve(root,relative);if(!target.startsWith(root+path.sep))throw new Error('Invalid path');
    const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.woff2':'font/woff2'}[path.extname(target)]||'application/octet-stream';
    res.writeHead(200,{'Content-Type':mime});res.end(await fs.readFile(target));
  }catch{res.writeHead(404);res.end();}});
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  browser=await chromium.launch({headless:true,args:['--no-sandbox'],...(args.browser?{executablePath:args.browser}:{})});
  const page=await browser.newPage({viewport:{width:1200,height:1000},deviceScaleFactor:1});
  page.on('pageerror',e=>console.error(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.waitForFunction(()=>window.run);
  const report=await page.evaluate(()=>window.run());
  await page.setViewportSize({width:Math.ceil(report.width),height:Math.ceil(report.height)});
  await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:path.join(temp,'preview.png')});
  await page.pdf({path:path.join(temp,'figure.pdf'),width:report.width+'px',height:report.height+'px',printBackground:true,
                 margin:{top:0,left:0,right:0,bottom:0}});
  const png=pngDpi(Buffer.from((await page.evaluate(()=>window.png)).split(',')[1],'base64'));
  report.pngWidth=png.readUInt32BE(16);report.pngHeight=png.readUInt32BE(20);
  report.sourceSha256=crypto.createHash('sha256').update(original).digest('hex');
  if(!(await fs.readFile(input)).equals(original))throw new Error('Source changed during export; retry using the current file');
  await fs.mkdir(path.dirname(prefix),{recursive:true});
  const sceneBytes=source.type==='excalidraw'?original:Buffer.from(JSON.stringify(await page.evaluate(()=>window.scene),null,2));
  if(input!==prefix+'.excalidraw')await fs.writeFile(prefix+'.excalidraw',sceneBytes);
  await fs.writeFile(prefix+'.svg',await page.evaluate(()=>window.svgText));
  await fs.writeFile(prefix+'.png',png);
  await fs.copyFile(path.join(temp,'figure.pdf'),prefix+'.pdf');
  await fs.copyFile(path.join(temp,'preview.png'),prefix+'_preview.png');
  await fs.writeFile(prefix+'_report.json',JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
}finally{
  if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve));
  await fs.rm(temp,{recursive:true,force:true});
}
