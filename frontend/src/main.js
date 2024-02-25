import './app.css';
// 웹 디자인을 위한 - 부트스트랩 적용 - 버젼은 5.대 버젼
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import App from './App.svelte';

const app = new App({
  target: document.getElementById('app'),
});

export default app;
