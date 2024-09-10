import qs from 'qs';
import { access_token, username, is_login } from './store';
import { get } from 'svelte/store';
import { push } from 'svelte-spa-router';

const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation;
    let content_type = 'application/json';
    let body = JSON.stringify(params);

    if (operation === 'login') {
        method = 'post';
        content_type = 'application/x-www-form-urlencoded';
        body = qs.stringify(params);
    }

    let _url = import.meta.env.VITE_SERVER_URL + url;
    if (method === 'get') {
        _url += '?' + new URLSearchParams(params);
    }

    let options = {
        method: method,
        headers: {
            'Content-Type': content_type
        }
    };

    const _access_token = get(access_token);
    if (_access_token) {
        options.headers['Authorization'] = 'Bearer ' + _access_token;  // 수정: Bearer 뒤에 공백 추가
    }

    if (method !== 'get') {
        options['body'] = body;
    }

    fetch(_url, options)
        .then(response => {
            if (response.status === 204) {
                if (success_callback) {
                    success_callback();
                }
                return;
            }

            // JSON 파싱 시 에러 처리를 추가하여 JSON 형식이 아닌 경우 대응
            return response.json().then(json => {
                if (response.status >= 200 && response.status < 300) {
                    if (success_callback) {
                        success_callback(json);
                    } else {
                        console.log('Success response:', json);  // success_callback이 없는 경우 기본 처리
                    }
                } else if (operation !== 'login' && response.status === 401) {
                    access_token.set('');
                    username.set('');
                    is_login.set(false);
                    alert('로그인이 필요합니다.');
                    push('/user-login');
                } else {
                    if (failure_callback) {
                        failure_callback(json);
                    } else {
                        console.error('Failure response:', json);  // failure_callback이 없는 경우 기본 처리
                        alert(JSON.stringify(json));
                    }
                }
            }).catch(error => {
                console.error('Error parsing JSON:', error);
                if (failure_callback) {
                    failure_callback({ message: 'JSON 파싱 오류' });
                } else {
                    alert('JSON 파싱 오류: ' + JSON.stringify(error));
                }
            });
        })
        .catch(error => {
            console.error('Fetch error:', error);
            if (failure_callback) {
                failure_callback({ message: '네트워크 오류' });
            } else {
                alert('네트워크 오류: ' + JSON.stringify(error));
            }
        });
};

export default fastapi;
