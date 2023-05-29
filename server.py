from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from main import main

# 警告 http.server本番環境には推奨されません。基本的なセキュリティ チェックのみを実装します 。
class Server(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self._set_headers()

    self.wfile.write(("<html><body><h1>GET message receive!</h1></body></html>").encode())

  def do_POST(self):
    self._set_headers()

    # アガリ情報をGETパラメータで受け取る
    parsed_path = urlparse(self.path)
    data = parse_qs(parsed_path.query)

    # 画像をPOSTのbodyで受け取る
    content_length = int(self.headers['Content-Length'])
    img = self.rfile.read(content_length)

    # jpgファイルにバイナリデータを書き込む
    with open("hai.jpg", mode="wb") as f:
      f.write(img)
      
    result = main(data, "hai.JPG")
    
    print(result)
  
    self.wfile.write(result.encode())
  

def run_http_server(server_class=HTTPServer, handler_class=Server, port=8000):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print('HTTP server started....')
  httpd.serve_forever()


if __name__ == '__main__':
  run_http_server()
