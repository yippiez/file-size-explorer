
import os

INVALID_FORM = """
        <form hx-post="/ls" hx-swap="outerHTML" class="bg-white shadow-md rounded-lg p-10 absolute top-1/4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="path-input">
                <span class="text-red-500">Invalid path.</span> Type your path and press enter to begin
            </label>
            <input
                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="path-input" type="text" name="path" placeholder="Path">
        </form>
"""


def get_type_of_path(file_path):
    _type = "file"
    if os.path.isdir(file_path):
        _type = "directory"
    return _type


def convertFilesListToHTML(files, path_prefix):
    html = ''

    html += '<div id="response-div" class="h-full w-8/12 p-4 m-4 rounded-lg bg-yellow-100">'

    parent_path = os.path.dirname(path_prefix)
    if parent_path != path_prefix:
        html += f"""
            <div class="m-3 flex justify-between bg-yellow-50 p-3 border-green-200 border-solid border-b-4">
                <form hx-post="/ls" hx-target="#response-div" hx-swap="outerHTML" class="flex w-full space-x-4 p-2">
                    <div class="relative"> 
                        <span class="fas fa-undo"></span> 
                        <input class="text-blue-500 mx-3 underline bg-opacity" type="submit" value="..">
                        <input class="absolute bg-transparent pointer-events-none left-8 top-6 text-xs whitespace-nowrap text-gray-600" 
                        type="text" name="path" value="{parent_path}" readonly>
                    </div>
                    
                </form>
            </div>
        """

    for file in files:
        full_path = os.path.join(path_prefix, file)
        _type = get_type_of_path(full_path)

        icon = ""
        match _type:
            case "file":
                icon = "fa-file"
            case "directory":
                icon = "fa-folder"
            case _:
                raise ValueError("Invalid type")

        html += f"""
        <div class="m-3 flex justify-between bg-yellow-50 p-3 border-green-200 border-solid border-b-4">
            <form hx-post="/ls" hx-target="#response-div" hx-swap="outerHTML" class="flex w-full space-x-4 p-2">
                <div class="relative"> 
                    <span class="fas {icon}"></span> 
        """

        if _type == "directory":
            html += f'<input class="text-blue-500 mx-3 underline bg-opacity" type="submit" value="{file}">'
        else:
            html += f'<span class="mx-3">{file}</span>'

        html += f"""
                    <input class="absolute bg-transparent pointer-events-none left-8 top-6 text-xs whitespace-nowrap text-gray-600" 
                    type="text" name="path" value="{full_path}" readonly>
                </div>
                
            </form>
            <div class="flex space-x-1">
                    <button class="whitespace-nowrap p-2 bg-white text-slate-800" hx-get="/size?q={full_path}" hx-trigger="click" hx-swap="innerHTML">Click to Calculate Size</button>
            </div>
        </div>
        """

    html += "</div>"

    return html
