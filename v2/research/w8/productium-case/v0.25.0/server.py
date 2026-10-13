"""Local-only Explorer service. Run: python server.py --port 8765."""
import argparse, json, secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit,parse_qs
from runtime import ROOT,VERSION,build_identity,connect,submit,history,record,export_nt

def make_server(port=8765,db_path=None):
    path = db_path or ROOT/'workspace.sqlite'
    db=connect(path);db.close()
    token=secrets.token_urlsafe(32)
    identity=build_identity()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def reply(self,status,obj,ctype='application/json'):
            raw=json.dumps(obj,ensure_ascii=False).encode() if ctype=='application/json' else obj.encode()
            self.send_response(status);self.send_header('Content-Type',ctype+'; charset=utf-8')
            self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(raw)
        def allowed_host(self):
            return self.headers.get('Host') in ['127.0.0.1:'+str(self.server.server_port),'localhost:'+str(self.server.server_port)]
        def do_GET(self):
            if not self.allowed_host():return self.reply(403,{'error':'LOCAL_HOST_REQUIRED'})
            url=urlsplit(self.path)
            if url.path=='/':
                return self.reply(200,(ROOT/'Explorer_Workbench_v0_25_0.html').read_text(),'text/html')
            if url.path=='/api/context':return self.reply(200,dict(build=identity,token=token,version=VERSION))
            db=connect(path)
            try:
                if url.path=='/api/history':return self.reply(200,history(db))
                if url.path=='/api/record':
                    row=record(db,parse_qs(url.query).get('id',[''])[0]);return self.reply(200 if row else 404,row or {'error':'UNKNOWN_RECORD'})
                if url.path=='/api/graph':
                    ws=parse_qs(url.query).get('workspace',[''])[0]
                    return self.reply(200,export_nt(db,ws),'application/n-triples')
                return self.reply(404,{'error':'NOT_FOUND'})
            finally:db.close()
        def do_POST(self):
            expected='http://'+self.headers.get('Host','')
            if not self.allowed_host() or self.headers.get('X-Explorer-Token')!=token or self.headers.get('Origin',expected)!=expected:
                return self.reply(403,{'error':'LOCAL_REQUEST_REQUIRED'})
            if self.path!='/api/transitions':return self.reply(404,{'error':'NOT_FOUND'})
            if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.reply(415,{'error':'JSON_REQUIRED'})
            try:size=int(self.headers.get('Content-Length','0'))
            except ValueError:return self.reply(400,{'error':'INVALID_LENGTH'})
            if not 0<size<=20000:return self.reply(413,{'error':'REQUEST_SIZE'})
            try:payload=json.loads(self.rfile.read(size))
            except (ValueError,UnicodeError):return self.reply(400,{'error':'INVALID_JSON'})
            db=connect(path)
            try:
                result=submit(db,payload);return self.reply(200,result)
            finally:db.close()
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);parser.add_argument('--db')
    args=parser.parse_args();server=make_server(args.port,args.db)
    print(f'Explorer {VERSION}: http://127.0.0.1:{server.server_port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
