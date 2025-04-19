import os
import re
import sys
import xml.etree.ElementTree as ET


def sanitize(name: str) -> str:
    """
    英数字、アンダースコア、ドット以外の文字をアンダースコアに置き換える
    """
    return re.sub(r'[^A-Za-z0-9_.]', '_', name)


def process_xml(xml_path: str):
    """
    train.xml をパースし、<task><name> および <image name> の属性値をサニタイズして更新する
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # <meta><task><name> の更新
        task_name_elem = root.find('.//meta/task/name')
        if task_name_elem is not None and task_name_elem.text:
            new_text = sanitize(task_name_elem.text)
            if new_text != task_name_elem.text:
                print(f"XML 更新: <task><name> '{task_name_elem.text}' -> '{new_text}'")
                task_name_elem.text = new_text

        # <image name="..."> の更新
        for img in root.findall('.//image'):
            name_attr = img.get('name')
            if name_attr:
                new_name = sanitize(name_attr)
                if new_name != name_attr:
                    print(f"XML 更新: image name '{name_attr}' -> '{new_name}'")
                    img.set('name', new_name)

        # 上書き保存
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)
    except ET.ParseError as e:
        print(f"XML パースエラー: {xml_path} - {e}")


def main():
    # ユーザーに対象ディレクトリを入力してもらう
    target_dir = input("対象とするディレクトリのパスを入力してください: ").strip()
    if not os.path.isdir(target_dir):
        print(f"エラー: '{target_dir}' は存在しないかディレクトリではありません。")
        sys.exit(1)

    # 深い階層から処理するために topdown=False を指定
    for root, dirs, files in os.walk(target_dir, topdown=False):
        # ファイルのリネーム
        for name in files:
            src_path = os.path.join(root, name)
            new_name = sanitize(name)
            if new_name != name:
                dst_path = os.path.join(root, new_name)
                if os.path.exists(dst_path):
                    print(f"警告: リネーム先 '{dst_path}' が既に存在します。スキップします。")
                else:
                    os.rename(src_path, dst_path)
                    print(f"リネーム: '{src_path}' -> '{dst_path}'")

        # ディレクトリのリネーム
        for name in dirs:
            src_path = os.path.join(root, name)
            new_name = sanitize(name)
            if new_name != name:
                dst_path = os.path.join(root, new_name)
                if os.path.exists(dst_path):
                    print(f"警告: リネーム先 '{dst_path}' が既に存在します。スキップします。")
                else:
                    os.rename(src_path, dst_path)
                    print(f"リネーム: '{src_path}' -> '{dst_path}'")

    # train.xml 内のパス・名前の更新
    for root, dirs, files in os.walk(target_dir):
        if 'train.xml' in files:
            xml_file = os.path.join(root, 'train.xml')
            process_xml(xml_file)

    print("処理が完了しました。")


if __name__ == "__main__":
    main()
