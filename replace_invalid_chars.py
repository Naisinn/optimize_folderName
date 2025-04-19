import os
import re
import sys


def main():
    # ユーザーに対象ディレクトリを入力してもらう
    target_dir = input("対象とするディレクトリのパスを入力してください: ").strip()
    # 存在チェック
    if not os.path.isdir(target_dir):
        print(f"エラー: '{target_dir}' は存在しないかディレクトリではありません。")
        sys.exit(1)

    # 深い階層から処理するために topdown=False を指定
    for root, dirs, files in os.walk(target_dir, topdown=False):
        # ファイルのリネーム
        for name in files:
            src_path = os.path.join(root, name)
            # 英数字、アンダースコア、ドット以外の文字をアンダースコアに置き換え
            new_name = re.sub(r'[^A-Za-z0-9_.]', '_', name)
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
            new_name = re.sub(r'[^A-Za-z0-9_.]', '_', name)
            if new_name != name:
                dst_path = os.path.join(root, new_name)
                if os.path.exists(dst_path):
                    print(f"警告: リネーム先 '{dst_path}' が既に存在します。スキップします。")
                else:
                    os.rename(src_path, dst_path)
                    print(f"リネーム: '{src_path}' -> '{dst_path}'")

    print("処理が完了しました。")


if __name__ == "__main__":
    main()