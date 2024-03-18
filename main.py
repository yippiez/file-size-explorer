import fastapi
import htmls
import os

HTML_FILE_PATH = "index.html"

app = fastapi.FastAPI()
last_content = ""
cache = {}


def sizeof_fmt(num, suffix="B"):
    # https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size

    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def get_size_of_folder(folder_path, acc=0):
    for path, dirs, files in os.walk(folder_path):
        for file in files:
            acc += os.path.getsize(os.path.join(path, file))
    return acc


def get_size_of_file(file_path):
    return os.path.getsize(file_path)


@app.get("/")
def read_root():
    return fastapi.responses.HTMLResponse(content=open(HTML_FILE_PATH, "r").read(), status_code=200)


@app.post("/ls")
async def read_path(path: str = fastapi.Form(...)):
    global last_content

    if not os.path.isdir(path):
        return fastapi.responses.HTMLResponse(content=htmls.INVALID_FORM, status_code=200)

    content = ""
    try:
        content = htmls.convertFilesListToHTML(os.listdir(path), path)
    except PermissionError:
        print("Permission denied")  # TODO: Replace with a proper error message
        return fastapi.responses.HTMLResponse(content=last_content, status_code=200)

    last_content = content

    return fastapi.responses.HTMLResponse(content=content, status_code=200)


@app.get("/size")
def read_size(q: str = fastapi.Query(...)):

    if cache.get(q):
        return fastapi.responses.HTMLResponse(content=cache[q], status_code=200)

    cache[q] = "Calculating..."

    if os.path.isdir(q):
        try:
            os.listdir(q)
        except PermissionError:
            return fastapi.responses.HTMLResponse(content="<span class='text-pink-500'>Requires Admin Access</span>", status_code=200)

        size_in_b = get_size_of_folder(q)
    else:
        size_in_b = get_size_of_file(q)

    size = sizeof_fmt(size_in_b)

    color = "green"
    if size_in_b > 1024 * 1024 * 1024:
        color = "red"
    elif size_in_b > 1024 * 1024:
        color = "yellow"

    html = f"""<span class="text-{color}-500">Size: {size}</span>"""

    cache[q] = html

    return fastapi.responses.HTMLResponse(content=html, status_code=200)
