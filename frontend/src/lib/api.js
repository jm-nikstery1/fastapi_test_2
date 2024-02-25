/**
 * 앞으로 만들 대부분의 기능들도 데이터 처리를 위해서는 위처럼 fetch 함수를 사용해야 한다.
 * fetch 함수에는 요청하는 URL 주소의 호스트명 처럼 공통적으로 사용할 수 있는 부분이 많다.
 * 따라서 데이터를 요청하는 함수를 공통 라이브러리로 만들어 사용하면 편리할 것이다.
 * 데이터 송수신을 위한 fastapi 함수를 작성
 *
 * api.js 파일안에 fastapi라는 함수를 생성
 * fastapi 함수의 매개변수
 *
 *  fastapi 함수를 사용할 때는 호스트명을 생략하고 그 뒷 부분만 전달
 *
 * OAuth2를 사용하여 로그인 할때 Content-Type을
 * application/x-www-form-urlencoded로 사용해야 하는 것은 OAuth2의 규칙
 */
import qs from 'qs';
import { access_token, username, is_login } from './store';
import {get} from 'svelte/store';
import {push} from 'svelte-spa-router';

const fastapi = (operation, url, params, success_callback, failure_callback) => {
  let method = operation; //데이터를 처리하는 방법, 소문자만 사용
  let content_type = 'application/json';
  let body = JSON.stringify(params);

  if (operation === 'login') {
    method = 'post';
    content_type = 'application/x-www-form-urlencoded';
    body = qs.stringify(params);
  } // application/x-www-form-urlencoded

  let _url = import.meta.env.VITE_SERVER_URL + url;
  if (method === 'get') {
    _url += '?' + new URLSearchParams(params);
  }

  let options = {
    method: method,
    headers: {
      'Content-Type': content_type,
    },
  };

  const _access_token = get(access_token)
  if(_access_token){
    options.headers["Authorization"] = "Beaer" + _access_token
  }

  if (method !== 'get') {
    options['body'] = body;
  }

  fetch(_url, options).then(response => {
    if (response.status === 204) {
      // no content
      // 답변에 응답 상태코드가 204인 경우에는 응답 결과가 없더라도 success_callback을 실행해야함
      if (success_callback) {
        success_callback();
      }
      return;
    }
    response
      .json()
      .then(json => {
        if (response.status >= 200 && response.status < 300) {
          //200~299
          if (success_callback) {
            success_callback(json);
          }
        } else if (operation !== 'login' && response.status ===401) {   //token time out
          access_token.set('')
          username.set('')
          is_login.set(false)
          alert("로그인이 필요합니다.")
          push('/user-login')

        } else {
          if (failure_callback) {
            failure_callback(json);
          } else {
            alert(JSON.stringify(json));
          }
        }
      })
      .catch(error => {
        alert(JSON.stringify(error));
      });
  });
};

export default fastapi;
