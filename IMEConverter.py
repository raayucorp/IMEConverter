import os
import sys
import plistlib
import math

def convert_msime_to_plist(input_file, output_file, split_size=None):
    """
    Convert a Microsoft IME dictionary file to macOS plist format.
    """
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct full paths
    input_path = os.path.join(script_dir, input_file)
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"エラー: 入力ファイル '{input_file}' が見つかりません。")
        print(f"現在のスクリプトディレクトリ: {script_dir}")
        print("ファイルが同じディレクトリにあることを確認してください。")
        sys.exit(1)
    
    # List to store dictionary entries
    dictionary_entries = []
    
    # Read the input file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            # Skip header lines starting with '!'
            lines = [line.strip() for line in f if not line.startswith('!')]
    except UnicodeDecodeError:
        print("エラー: ファイルの文字コードを確認してください。UTF-8でない可能性があります。")
        sys.exit(1)
    
    # Process each line
    processed_entries = set()
    for line in lines:
        # Split the line into components
        parts = line.split('\t')
        
        # Ensure we have at least 2 parts (shortcut and phrase)
        if len(parts) >= 2:
            shortcut = parts[0]
            phrase = parts[1]
            
            # Avoid duplicate entries
            if (shortcut, phrase) not in processed_entries:
                # macOS用の形式に合わせて調整
                dictionary_entries.append({
                    "phrase": phrase,
                    "shortcut": shortcut
                })
                processed_entries.add((shortcut, phrase))
    
    # If no splitting is required
    if split_size is None or split_size >= len(dictionary_entries):
        output_path = os.path.join(script_dir, output_file)
        try:
            with open(output_path, 'wb') as f:
                # macOS用のplist形式に合わせて調整
                plistlib.dump(dictionary_entries, f, fmt=plistlib.FMT_XML)
            
            print(f"変換完了。{len(dictionary_entries)}エントリを {output_file} に書き出しました。")
        except Exception as e:
            print(f"出力ファイルの書き出し中にエラーが発生しました: {e}")
            sys.exit(1)
    else:
        # Split entries into multiple files
        num_files = math.ceil(len(dictionary_entries) / split_size)
        
        for i in range(num_files):
            start_idx = i * split_size
            end_idx = min((i + 1) * split_size, len(dictionary_entries))
            
            # Create filename with index
            split_output_file = f"{os.path.splitext(output_file)[0]}_{i+1}.plist"
            output_path = os.path.join(script_dir, split_output_file)
            
            try:
                with open(output_path, 'wb') as f:
                    # macOS用のplist形式に合わせて調整
                    plistlib.dump(dictionary_entries[start_idx:end_idx], f, fmt=plistlib.FMT_XML)
                
                print(f"分割ファイル {split_output_file} に {end_idx - start_idx} エントリを書き出しました。")
            except Exception as e:
                print(f"{split_output_file} の書き出し中にエラーが発生しました: {e}")
                sys.exit(1)
        
        print(f"合計 {num_files} 個のplistファイルに分割しました。")

def main():
    # スクリプト実行時の対話型インターフェース
    print("Microsoft IME辞書をmacOS plistに変換します。")
    
    # 入力ファイル名
    input_file = input("入力ファイル名を入力してください (デフォルト: msime.txt): ").strip() or 'msime.txt'
    
    # 出力ファイル名
    output_file = input("出力ファイル名を入力してください (デフォルト: output.plist): ").strip() or 'output.plist'
    
    # 分割するかどうか
    split_choice = input("plistファイルを分割しますか？ (y/N): ").strip().lower()
    
    split_size = None
    if split_choice == 'y':
        while True:
            try:
                split_size = int(input("1つのplistファイルに含める項目数を入力してください: "))
                if split_size > 0:
                    break
                else:
                    print("1以上の数値を入力してください。")
            except ValueError:
                print("有効な数値を入力してください。")
    
    # 変換処理の実行
    convert_msime_to_plist(input_file, output_file, split_size)

# スクリプト実行時のエントリーポイント
if __name__ == '__main__':
    main()