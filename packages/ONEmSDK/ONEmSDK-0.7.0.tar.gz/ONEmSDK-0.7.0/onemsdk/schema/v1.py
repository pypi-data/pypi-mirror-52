from enum import Enum
from typing import List, Union, Optional

from pydantic import BaseModel, Schema

from onemsdk.exceptions import ONEmSDKException
from onemsdk.parser import (FormTag, SectionTag, LiTag, PTag, BrTag, UlTag,
                            ATag, HeaderTag, FooterTag, InputTag)
from onemsdk.parser.tag import InputTagType


class MenuItemType(str, Enum):
    option = 'option'
    content = 'content'


class HttpMethod(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'


class MenuItem(BaseModel):
    """
    An item in a menu. Depending on its type, a menu item can be either an option (type=option) or an option separator (type=content)
    """
    type: MenuItemType = Schema(
        ...,
        description='The type of the menu item.'
    )
    description: str = Schema(
        ...,
        description='The displayed text of a menu item.'
    )
    text_search: str = Schema(
        None,
        description='Field to add more context for searching in options'
    )
    method: HttpMethod = Schema(
        None,
        description='The HTTP method called when the menu item is selected.'
    )
    path: str = Schema(
        None,
        description='The path called when the menu item is selected.'
    )

    def __init__(self, description: str, text_search: str = None,
                 method: HttpMethod = None, path: str = None):
        if path:
            type = MenuItemType.option
            method = method or HttpMethod.GET
        else:
            type = MenuItemType.content
        super(MenuItem, self).__init__(type=type, description=description,
                                       text_search=text_search, method=method, path=path)

    @classmethod
    def from_tag(cls, tag: Union[LiTag, PTag, BrTag, str]) -> Optional['MenuItem']:
        if isinstance(tag, str):
            description = tag
        else:
            description = tag.render()

        if not description:
            return None

        method = None
        path = None
        text_search = None

        if isinstance(tag, LiTag) and isinstance(tag.children[0], ATag):
            atag: ATag = tag.children[0]
            method = atag.attrs.method
            path = atag.attrs.href
            text_search = tag.attrs.text_search

        return MenuItem(description=description, text_search=text_search, method=method,
                        path=path)


MenuItem.update_forward_refs()


class MenuMeta(BaseModel):
    """
    Configuration fields for `Menu`
    """
    auto_select: bool = Schema(
        False,
        description='If the `Menu` has only one option, it is automatically selected, '
                    'without asking the user for selection'
    )


MenuMeta.update_forward_refs()


class Menu(BaseModel):
    """
    A top level component that permits displaying a navigable menu or a plain text.
    """
    type: str = Schema(
        'menu',
        description='The type of the Menu object is always "menu"',
        const=True
    )
    body: List[MenuItem] = Schema(..., description='The body/content of the menu')
    header: str = Schema(None, description='The header of the menu.')
    footer: str = Schema(None, description='The header of the menu.')

    meta: MenuMeta = Schema(None, description='Configuration fields for `Menu`')

    def __init__(self, body: List[MenuItem], header: str = None, footer: str = None,
                 meta: MenuMeta = None):
        super(Menu, self).__init__(type='menu', body=body, header=header, footer=footer,
                                   meta=meta)

    @classmethod
    def from_tag(cls, section_tag: SectionTag) -> 'Menu':
        body = []
        header = None
        footer = None

        for child in section_tag.children:
            if isinstance(child, UlTag):
                body.extend([MenuItem.from_tag(li) for li in child.children])
            elif isinstance(child, HeaderTag):
                header = child.render()
            elif isinstance(child, FooterTag):
                footer = child.render()
            else:
                body.append(MenuItem.from_tag(child))

        return Menu(
            body=list(filter(None, body)),
            header=header or section_tag.attrs.header,
            footer=footer or section_tag.attrs.footer,
            meta=MenuMeta(
                auto_select=section_tag.attrs.auto_select
            )
        )


Menu.update_forward_refs()


class FormItemType(str, Enum):
    string = 'string'  # the user should enter a string during this step
    date = 'date'  # the user should enter a date
    datetime = 'datetime'  # the user should enter a date and a time
    hidden = 'hidden'  # will not be displayed to the user
    int = 'int'  # the user should enter an integer
    float = 'float'  # the user could enter a floating number
    form_menu = 'form-menu'  # the user should choose an option from the menu
    email = 'email'  # the user should send a valid email address
    url = 'url'  # the user should send a valid url
    location = 'location'  # the user should send a valid location


class MenuItemFormItem(BaseModel):
    """
    An item in a form's menu
    """
    type: MenuItemType = Schema(
        ...,
        description='The type of a menu item inside a form'
    )
    description: str = Schema(..., description='The description of this MenuItemFormItem')
    value: str = Schema(
        None,
        description='The value of this MenuItemFormItem, used in form serialization'
    )
    text_search: str = Schema(
        None,
        description='Field to add more context for searching in options'
    )

    def __init__(self, description: str, value: str = None, text_search: str = None):
        if value:
            type = MenuItemType.option
        else:
            type = MenuItemType.content
        super(MenuItemFormItem, self).__init__(
            type=type, description=description, value=value, text_search=text_search
        )

    @classmethod
    def from_tag(cls, tag: Union[LiTag, PTag, BrTag, str]
                 ) -> Union['MenuItemFormItem', None]:
        value = None
        text_search = None

        if isinstance(tag, str):
            description = tag
        else:
            description = tag.render()

        if not description:
            return None

        if isinstance(tag, LiTag):
            value = tag.attrs.value
            text_search = tag.attrs.text_search

        return MenuItemFormItem(value=value, description=description,
                                text_search=text_search)


MenuItemFormItem.update_forward_refs()


class MenuFormItemMeta(BaseModel):
    """
    Configuration fields for a `FormItem`
    """
    auto_select: bool = Schema(
        False,
        description='Will be automatically selected if set to true and in case of a '
                    'single option in the menu'
    )
    multi_select: bool = Schema(
        False,
        description='It allows multiple options to be selected'
    )
    numbered: bool = Schema(
        False,
        description='Display numbers instead of letter option markers'
    )


MenuFormItemMeta.update_forward_refs()


class FormItem(BaseModel):
    """
    Component used to ask a user for a certain type of free input
    """
    type: FormItemType = Schema(
        ...,
        description='The type of data expected from the user'
    )
    name: str = Schema(
        ...,
        description='The name of this FormItem, used in form serialization'
    )
    description: str = Schema(..., description='The description of this FormItem')
    header: str = Schema(None, description='If provided will overwrite the Form.header')
    footer: str = Schema(None, description='If provided will overwrite the Form.footer')
    body: List['MenuItemFormItem'] = Schema(
        None,
        description='Required only for type=form-menu'
    )
    value: str = Schema(
        None,
        description='Required for type=hidden'
    )
    chunking_footer: str = Schema(
        None,
        description='Shown in the footer of the sms chunks'
    )
    confirmation_label: str = Schema(
        None,
        description='Shown in the confirmation menu'
    )
    min_length: int = Schema(
        None,
        description='Validates the user input - for type=string'
    )
    min_length_error: str = Schema(
        None,
        description='Message to be shown on min_length error'
    )
    max_length: int = Schema(
        None,
        description='Validates the user input - for type=string'
    )
    max_length_error: str = Schema(
        None,
        description='Message to be shown on max_length error'
    )
    min_value: float = Schema(
        None,
        description='Validates the user input - for type=int|float'
    )
    min_value_error: str = Schema(
        None,
        description='Message to be shown on min_value error'
    )
    max_value: float = Schema(
        None,
        description='Validates the user input - for type=int|float'
    )
    max_value_error: str = Schema(
        None,
        description='Message to be shown on max_value error'
    )
    meta: 'MenuFormItemMeta' = Schema(
        None,
        description='Applies only for type=form-menu'
    )
    method: HttpMethod = Schema(
        None,
        description='http method, how the callback url should be triggered'
    )
    required: bool = Schema(
        False,
        description='Can be skipped if set to false'
    )
    status_exclude: bool = Schema(
        False,
        description='If true this step will be excluded from the form completion status'
    )
    status_prepend: bool = Schema(
        False,
        description='If true this step will be prepended to the body pre of the response - appended otherwise'
    )
    url: str = Schema(
        None,
        description='Callback url triggered right after the choice has been set for this form item'
    )
    validate_type_error: str = Schema(
        None,
        description='An error message to be shown on basic type validation'
    )
    validate_type_error_footer: str = Schema(
        None,
        description='Shown in the error message footer'
    )
    validate_url: str = Schema(
        None,
        description='the callback url path (GET) triggered to validate user input with '
                    'query string ?name=user_input - url must return json content '
                    '{"valid": True/False, "error": "Some validation error message"}'
    )

    def __init__(self, **data):
        super(FormItem, self).__init__(**data)

    @classmethod
    def from_tag(cls, section: SectionTag) -> 'FormItem':
        header = None
        footer = None
        body = []
        value = None
        min_value = None
        min_value_error = None
        min_length = None
        min_length_error = None
        max_value = None
        max_value_error = None
        max_length = None
        max_length_error = None

        content_types_map = {
            InputTagType.date: FormItemType.date,
            InputTagType.datetime: FormItemType.datetime,
            InputTagType.text: FormItemType.string,
            InputTagType.hidden: FormItemType.hidden,
            InputTagType.email: FormItemType.email,
            InputTagType.location: FormItemType.location,
            InputTagType.url: FormItemType.url,
        }

        for child in section.children:
            if isinstance(child, InputTag):
                input_type = child.attrs.type

                # HTML does not have type "int" or "float", it has "number"
                # If the input type is "number", determine if it's "int" or "float"
                if input_type == InputTagType.number:
                    if child.attrs.step == 1:
                        content_types_map[InputTagType.number] = FormItemType.int
                    else:
                        content_types_map[InputTagType.number] = FormItemType.float

                # Check if hidden input declares attribute "value"
                if input_type == InputTagType.hidden:
                    value = child.attrs.value
                    if value is None:
                        raise ONEmSDKException(
                            'value attribute is required for input type="hidden"'
                        )

                min_value = child.attrs.min
                min_value_error = child.attrs.min_error
                min_length = child.attrs.minlength
                min_length_error = child.attrs.minlength_error
                max_value = child.attrs.max
                max_value_error = child.attrs.max_error
                max_length = child.attrs.maxlength
                max_length_error = child.attrs.maxlength_error

                # Ignore other <input> tags if exist
                break
            if isinstance(child, UlTag):
                # Hack with an invalid input type to avoid KeyError
                input_type = 'option'
                content_types_map[input_type] = FormItemType.form_menu
                for li in child.children:
                    body.append(MenuItemFormItem.from_tag(li))
                break
        else:
            raise ONEmSDKException(
                'When <section> plays the role of a form item, '
                'it must contain a <input/> or <ul></ul>'
            )

        if isinstance(section.children[0], HeaderTag):
            header = section.children[0].render()
        if isinstance(section.children[-1], FooterTag):
            footer = section.children[-1].render()

        return FormItem(
            type=content_types_map[input_type],
            name=section.attrs.name,
            description=section.render(exclude_header=True, exclude_footer=True),
            header=header or section.attrs.header,
            footer=footer or section.attrs.footer,
            body=body or None,
            value=value,
            chunking_footer=section.attrs.chunking_footer,
            confirmation_label=section.attrs.confirmation_label,
            min_value=min_value,
            min_value_error=min_value_error,
            min_length=min_length,
            min_length_error=min_length_error,
            max_value=max_value,
            max_value_error=max_value_error,
            max_length=max_length,
            max_length_error=max_length_error,
            meta=MenuFormItemMeta(
                auto_select=section.attrs.auto_select,
                multi_select=section.attrs.multi_select,
                numbered=section.attrs.numbered,
            ),
            method=section.attrs.method,
            required=section.attrs.required,
            status_exclude=section.attrs.status_exclude,
            status_prepend=section.attrs.status_prepend,
            url=section.attrs.url,
            validate_type_error=section.attrs.validate_type_error,
            validate_type_error_footer=section.attrs.validate_type_error_footer,
            validate_url=section.attrs.validate_url,
        )


FormItem.update_forward_refs()


class FormMeta(BaseModel):
    """
    Configuration fields for a Form
    """
    completion_status_show: bool = Schema(
        False,
        title='Show completion status',
        description='Whether to display the completions status'
    )
    completion_status_in_header: bool = Schema(
        False,
        title='Show completion status in header',
        description='Whether to display the completion status in header'
    )
    confirmation_needed: bool = Schema(
        False,
        title='Confirmation needed',
        description='Whether to add an additional item at the end of the form for confirmation'
    )

    def __init__(self,
                 completion_status_show: bool = False,
                 completion_status_in_header: bool = False,
                 confirmation_needed: bool = False):
        super(FormMeta, self).__init__(
            completion_status_in_header=completion_status_in_header,
            completion_status_show=completion_status_show,
            confirmation_needed=confirmation_needed
        )


FormMeta.update_forward_refs()


class Form(BaseModel):
    """
    A top level component used to acquire information from user
    """
    type: str = Schema('form', description='The type of a form is always form',
                       const=True)
    body: List[FormItem] = Schema(
        ...,
        description='Sequence of components used to acquire the pieces of data needed from user'
    )
    method: HttpMethod = Schema(
        HttpMethod.POST,
        description='The HTTP method used to send the form data'
    )
    path: str = Schema(..., description='The path used to send the form data')
    header: str = Schema(
        None,
        description='The header of the form. It can be overwritten by each body component'
    )
    footer: str = Schema(
        None,
        description='The footer of the form. It can be overwritten by each body component'
    )
    meta: FormMeta = Schema(None, description='Contains configuration flags')

    @classmethod
    def from_tag(cls, form_tag: FormTag) -> 'Form':
        body = []
        for section in form_tag.children:
            body.append(FormItem.from_tag(section))

        form = Form(
            header=form_tag.attrs.header,
            footer=form_tag.attrs.footer,
            meta=FormMeta(
                completion_status_show=form_tag.attrs.completion_status_show,
                completion_status_in_header=form_tag.attrs.completion_status_in_header,
                confirmation_needed=form_tag.attrs.confirmation_needed
            ),
            method=form_tag.attrs.method,
            path=form_tag.attrs.action,
            body=body
        )
        return form


Form.update_forward_refs()


class MessageContentType(str, Enum):
    form = 'form'
    menu = 'menu'


class Response(BaseModel):
    """
    A JSON-serialized instance of Response must be sent as response to the ONEm platform. It can be built only from a top level object (Menu, Form).
    """
    content_type: MessageContentType = Schema(
        ...,
        title='Content type',
        description='The type of the content of the response'
    )
    content: Union[Form, Menu] = Schema(
        ...,
        description='The content of the response'
    )

    def __init__(self, content: Union[Menu, Form]):
        if isinstance(content, Menu):
            content_type = MessageContentType.menu
        elif isinstance(content, Form):
            content_type = MessageContentType.form
        else:
            raise ONEmSDKException(f'Cannot create response from {type(content)}')

        super(Response, self).__init__(content_type=content_type, content=content)

    @classmethod
    def from_tag(cls, tag: Union[FormTag, SectionTag]):
        if isinstance(tag, FormTag):
            return Response(content=Form.from_tag(tag))
        if isinstance(tag, SectionTag):
            return Response(content=Menu.from_tag(tag))
        raise ONEmSDKException(f'Cannot create response from {tag.Config.tag_name} tag')


Response.update_forward_refs()
