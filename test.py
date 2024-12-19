@app.route('/upload_image', methods=['PUT'])
def upload_image():
    received_data = []
    boundary = None

    # Content-Typeヘッダーから境界を取得
    content_type = request.headers.get('Content-Type')
    if content_type:
        parts = content_type.split(';')
        for part in parts:
            if 'boundary=' in part:
                boundary = part.split('=')[1].strip()
                break

    if not boundary:
        return jsonify({'error': 'Content-Typeヘッダーに境界がありません'}), 400

    # 境界まで読み込む
    while True:
        chunk = request.stream.readline()
        if not chunk:
            return jsonify({'error': 'データが不完全です'}), 400

        if chunk.startswith(f'----{boundary}--'.encode()):
            break

        if chunk.startswith(f'----{boundary}'.encode()):
            continue

        received_data.append(chunk)

    # 受信したデータを結合し、Base64デコード
    data = b''.join(received_data)
    # ここで、Base64デコード処理を記述
    base64_image = extract_base64_data(data)  # 例えば、正規表現などでBase64部分を抽出
    img_data = base64.b64decode(base64_image)

    with open('./uploaded_image.jpg', 'wb') as f:
        f.write(img_data)
        print("画像が正常にアップロードされました！")

    return jsonify({'status': 'ok'})
