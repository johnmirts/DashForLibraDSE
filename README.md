# DashForLibraDSE

### Video tutorials:
YouTube playlist: https://www.youtube.com/playlist?list=PLYD54mj9I2JevdabetHsJ3RLCeMyBNKYV

### Reading resources:
- [Amazon](https://www.amazon.com/Interactive-Dashboards-Data-Apps-Plotly/dp/1800568916/ref=pd_bxgy_d_sccl_1/139-8681413-1867921?pd_rd_w=hZwpa&content-id=amzn1.sym.c51e3ad7-b551-4b1a-b43c-3cf69addb649&pf_rd_p=c51e3ad7-b551-4b1a-b43c-3cf69addb649&pf_rd_r=2PPSWYKTPGSXCHVCSNAN&pd_rd_wg=ZFZSl&pd_rd_r=14f6b522-149e-4a9c-a83e-1a73d3b4a80a&pd_rd_i=1800568916&psc=1), book by ELias Dabbas.

- [The book of Dash](https://nostarch.com/book-dash), book by Adam Schroeder.

### Community forum: 
https://community.plotly.com/c/python/25

### Plotly documentation
https://dash.plotly.com/

### Plotly Main Graphing Libraries
https://plotly.com/python/plotly-fundamentals/

### Plotly Python API references
https://plotly.com/python-api-reference/index.html

### Advanced layout and UX
https://dash-bootstrap-components.opensource.faculty.ai/

---

### Deployed example on Render with data coming in through http link: deploy-app-example-repo
 
#### Prepare your App on Pycharm: 
1. Open Pycharm and activate venv: `.\venv\Scripts\activate`
2. Install all libraries and `gunicorn` in your virtual environment
3. Create requirements file: `pip freeze > requirements.txt`
4. Make sure your app code has `server = app.server`
5. Run app to make sure it works: `python app.py`
6. Push code to your github account: https://youtu.be/vpRkAoCqX3o 

#### Deploy App to the Web with Render: https://youtu.be/H16dZMYmvqo?feature=shared 
7. Open your Render account
8. Create new Web Service and choose: “Build and deploy from a Git repository”
9. Add the url of your public git repository
10. Give the app a unique name
11. Update the gunicorn command to: `gunicorn app_name:server`

Possible error: Render won’t work with the latest version of certain python libraries. For example, you’ll get an error if your requirements.txt file has the most recent version of pandas. Render allows up to pandas==1.3.5

#### Deployed example on Render with data in local csv sheet: deploy-app2-example-repo

- When your app has a local csv sheet you’re pulling data from, the file structure should look like this: deploy-app2-example-repo
- Notice how you would read the csv sheet into your app
- Don’t forget to add to your app code: `server = app.server`
- And install `gunicorn` in your virtual environment\
- When deploying the app on Render.com, ensure that the Root Directory is `src`
