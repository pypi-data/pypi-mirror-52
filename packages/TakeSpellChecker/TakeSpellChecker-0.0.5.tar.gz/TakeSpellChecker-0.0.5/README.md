# TakeSpellChecker

TakeSpellChecker is a package that checks the spelling of words in any language using machine learning. It corrects the misspelled word by combining the context of the surrounding words to predict a list of the probable words and finds the one with the highest character similarity. The solution uses word embedding to learn the context. So, it's required to pass the path of the word embedding file. Also supports optionally to pass a configuration file (if the file is in an Azure fileshare, in other words, if the parameter from_azure is true).

#### TakeSpellChecker.SpellCheck: create constructor

<ul>
<li>path: str</li>
path is the full embedding path to your word embedding model. Optionally, you can also set from_azure as True and pass a configuration file path to path.

<li>from_azure: boolean</li>
from_azure is an optional parameter. If you need to automatically download an embedding model from azure file share, you need to set this parameter as True and pass a configuration file to path instead of an embedding file.
</ul>

#### TakeSpellChecker.set_data: sets the data

<ul>
<li>data: list, series, dataframe or a string that represents the file path</li>
data is the content that needs to be processed. It can be a list, series, string or dataframe.

<li>content_column_name: str</li>
content_column_name is an optional parameter. It's only required when the data's type is a Dataframe or a path to the text file. If the column name is not set, the set_data method uses the first column as content

<li>file_sep: str</li>
file_sep is an optional parameter. It's only required when the data's is a path to the text file. If the file separator is not set, the set_data uses ';'.

<li>encoding: str</li>
encoding is an optional parameter. It's only required when the data's is a path to the text file. If the file encoding is not set, the set_data uses 'utf-8'.
</ul>

#### TakeSpellChecker.spell_check: checks the spelling of the data

<ul>
<li>window_limit: int</li>
window_limit is an optional parameter. Used to determine how many words of the sentence will be used as context.

<li>threshold: float</li>
threshold is an optional parameter. Used to determine how permissive your spell checker will be.

<li>save_result: boolean</li>
save_result is an optional parameter. If save_result is True, a file (output_spell_check.csv) with the columns: Original, SpellChecked and Corrected will be created in the same directory. The last column is an boolean column indicating if any word in the sentence was corrected.

<li>output_file_name: str</li>
output_file_name is an optional parameter. If save_result is True and output_file_name is set, the file will output_spell_check.csv) with the columns: Original, SpellChecked and Corrected will be created in the same directory
</ul>

## config.yml
```
account_name: my_account_name
account_key: my_key
directory: my_directory_name
embedding_file: my_embedding_file_name
embedding_share: my_file_share_name
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install TakeSpellChecker

```bash
pip install TakeSpellChecker
```

## Usage

```python
import TakeSpellChecker as sc

spell_checker = sc.SpellCheck(path, from_azure = True)
spell_checker.set_data(data)
corrected_df = spell_checker.spell_check(window_limit = 5, threshold = 0.94, save_result = True)
print(corrected_df)
```

## Author
Karina Tiemi Kato

## License
[MIT](https://choosealicense.com/licenses/mit/)
