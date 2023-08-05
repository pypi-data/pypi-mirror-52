# History

---
## 0.6.0
- Decreased the minimum Python version to 3.6.

- HTML API:
  - Added a bunch of new attributes on `<input>`: `min`, `min_error`,
  `minlength`, `minlength_error`, `max`, `max_error`, `maxlength`,
  `maxlength_error`, `step`, `value`
  - Added a bunch of new attributes on `<section>`: `chunking_footer`,
  `confirmation_label`, `method`, `required`, `status_exclude`,
  `status_prepend`, `url`, `validate_type_error`, `validate_type_error_footer`,
  `validate_url`
  - Added new input types: `number`, `hidden`
  - Added `text-search` attribute on `<li>`

- Python API
  - Removed `FormItemMenu` and `FormItemContent`. Use a single model instead -
  `FormItem` which achieves the functionality of both old models
  - A bunch of new properties were added on `FormItem`, taken from `<input>`
  and `<section>` tags (see changes in HTML API above).
  - Added `text_search` property on `MenuItemFormItem`

- Fixes:
  - Fix some bad tests
---
## 0.5.0
- HTML API:
  - Added `auto-select`, `multi-select` and `numbered` flags on `<section>` 
  tag. They take effect only if the `<section>` tag contains options
  - Boolean attributes are evaluated according to HTML5 (if present, a boolean
  attribute is true; if absent, it's false)

- Python API:
  - Added `MenuMeta` and `FormItemMenuMeta` objects to describe `Menu` objects 
  and `FormItemMenu` objects respectively.
    - `MenuMeta` can contain `auto_select`
    - `FormItemMenuMeta` can contain `auto_select`, `multi_select` and `numbered`
    - these attributes have origin in `<section>` tag
---
