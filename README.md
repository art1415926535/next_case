# Next case, please

Snake case ➡ Screaming snake case ➡ Camel case ➡ Snake case ➡ Screaming snake case ➡ Camel case ➡ ...

# Usage
1. Update file:
   ```
   Next_case.exe file line_number start_column end_column
   ```
1. Copy to clipboard:
   ```
   Next_case.exe copy MyVariable
   ```

# Integration
## PyCharm
### Create external tool
1. File ➡ Settings ➡ Tools ➡ External Tools ➡ ➕

2. Create tool
   * Name: `Next_case`
   * Program: `<path to Next_case.exe>`
   * Arguments: `file "$FilePath$" $SelectionStartLine$ $SelectionStartColumn$ $SelectionEndColumn$`
   * Uncheck: Open console for tool output

### Add hotkey
1. File ➡ Keymap ➡ 🔍 _Next_case_
2. Add preferred hotkey.


# Building from source
1. Install PyInstaller:
   ```
   pip install PyInstaller
   ```
1. Build executable file:
   ```
   pyinstaller next_case\main.py --onefile -n Next_case -i icon.ico
   ```
