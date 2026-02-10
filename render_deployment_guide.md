# Deploying FastAPI to Render

Follow these steps to deploy your application to Render.

## 1. Prepare your Repository
Ensure your latest changes are pushed to GitHub.

## 2. Create a Web Service on Render
1.  Log in to [Render](https://render.com/).
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub repository.

## 3. Configure the Web Service
- **Name:** Choose a name for your service.
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`

## 4. Environment Variables
If your application uses a `.env` file, you must add these variables in the **Environment** tab on Render.

> [!IMPORTANT]
> Do not upload your `.env` file to GitHub. Instead, manually add the keys and values in the Render dashboard.

## 5. Deployment
Render will automatically deploy your application once you click **Create Web Service**. You can monitor the logs in the Render dashboard.

## Local Verification
To test the production command locally (Linux/macOS recommended):
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```
Note: Gunicorn does not natively support Windows. For Windows development, continue using `uvicorn main:app --reload`.
