from flask import Flask, render_template, request
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)

class MyQr:
    def __init__(self, size: int, padding: int) -> None:
        self.size = size
        self.padding = padding

    def create_qr_base64(self, user_input: str, fg: str, bg: str) -> str:
        try:
            qr = qrcode.QRCode(box_size=self.size, border=self.padding)
            qr.add_data(user_input)
            qr.make(fit=True)

            img = qr.make_image(fill_color=fg, back_color=bg)

            img_byte_array = BytesIO()
            img.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)

            encoded_img = base64.b64encode(img_byte_array.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_img}"
        except Exception as e:
            print(f'Error: {e}')
            return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    if request.method == 'POST':
        user_input = request.form.get('text_input')  # Assuming a form field with name 'text_input'

        myqr = MyQr(size=30, padding=2)
        qr_image_base64 = myqr.create_qr_base64(user_input, fg='black', bg='white')

        return render_template('show_qr.html', qr_image_base64=qr_image_base64)

if __name__ == '__main__':
    app.run(debug=True)
