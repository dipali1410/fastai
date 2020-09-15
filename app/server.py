import aiohttp
import asyncio
import uvicorn
import numpy #
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

export_file_url = 'https://www.googleapis.com/drive/v3/files/1-46Jl_ZLstBUgfDX3A39zuuLLdtX5BrB?alt=media&key=AIzaSyDxvX7eErCuHbuZNAOXKKCHL_eRCynOq_I'
export_file_name = 'export.pkl'

classes = ['Jacob Elordi or Noah',
 'Joel Courtney or Lee',
 'Joey King or Elle',
 'Maise Richardson-sellers or Chloe',
 'Meganne Young or Rachel',
 'Molly Ringwald known or Sara Flynn',
 'Taylor Zakhar Perez or Marco']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction, pred_idx, probs = learn.predict(img)
    probability = str(round(float((max(probs)*100).numpy()), 2)) + "%"
    if prediction == 'Jacob Elordi or Noah':
     url = "https://i.insider.com/5f22ebfe19182415af6d1122?width=1100&format=jpeg&auto=webp"
    elif prediction == 'Joel Courtney or Lee':
     url = "https://i.pinimg.com/originals/38/20/70/3820706a112ac32ae61f0b8f6557c6e6.jpg"
    elif prediction == 'Joey King or Elle':
     url = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/joey-king-index-social-1-1596649980.png"
    elif prediction == 'Maise Richardson-sellers or Chloe':
     url = "https://assets.popbuzz.com/2020/29/who-plays-chloe-winthrop-in-the-kissing-booth-2---maisie-richardson-sellers-1595579770-view-0.png"
    elif prediction == 'Meganne Young or Rachel':
     url = "https://u6c3f6j7.rocketcdn.me/wp-content/uploads/2020/07/Meganne-Young.jpg"
    elif prediction == 'Molly Ringwald known or Sara Flynn':
     url = "https://s.yimg.com/ny/api/res/1.2/znXmy0unC5NjdHwkxHrWvg--~A/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9ODAw/http://media.zenfs.com/en/homerun/feed_manager_auto_publish_494/5ac89786c8bc4a636404db2f996b725c"
    else:
     url = "https://i.pinimg.com/736x/fe/3f/fa/fe3ffa0fa9b2c08ff4b2a1cab75670dc.jpg"
     
    return JSONResponse({'result': str(prediction), 'probability': str(probability), 'url': str(url)})
 


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
