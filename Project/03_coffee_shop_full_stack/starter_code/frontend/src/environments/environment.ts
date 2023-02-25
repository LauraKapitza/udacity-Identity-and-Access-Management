export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-udacity-lk.eu', // the auth0 domain prefix
    audience: 'http://127.0.0.1:5000/login', // the audience set for the auth0 app
    clientId: '41pWZ4tOKGXdREGs5yT9LUITSJdEhT2w', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application.
  }
};
