import { user, access_token, questions ,is_loading,gpt_response, is_loading2} from './store';
import fastapi from './api.js';

export async function login(username, password) {
    return new Promise((resolve, reject) => {
        fastapi('login', '/api/user/login', { username, password }, (data) => {
            user.set(data);
            access_token.set(data.access_token);
            localStorage.setItem('access_token', data.access_token);
            fetchMyQuestions()
                .then(() => resolve())
                .catch((error) => reject(error));
        }, (error) => {
            reject(error);
        });
    });
}

export async function fetchMyQuestions() {
    return new Promise((resolve, reject) => {
        fastapi('get', '/api/question/user_list', {}, (data) => {
            questions.set(data);
            resolve(data);
        }, (error) => {
            reject(error);
        });
    });
}

export async function sendPrompt(question, category) {
    console.log('Sending prompt:', question);
    is_loading.set(true); // 로딩 시작
    return new Promise((resolve, reject) => {
        fastapi('post', '/api/question/gpt', { question, category }, (data) => {
            console.log('Received response:', data);
            gpt_response.set(data.response);
            is_loading.set(false); // 로딩 끝
            resolve(data);
        }, (error) => {
            console.error('Error sending prompt:', error);
            is_loading.set(false); // 로딩 끝
            reject(error);
        });
    });
}

export async function makeText(question, keyword) {
    is_loading2.set(true);
    return new Promise((resolve, reject) => {
        fastapi('post', '/api/question/text', { question, keyword }, (data) => {
            is_loading2.set(false);
            gpt_response.set(data.response);
            resolve(data);
        }, (error) => {
            is_loading2.set(false);
            reject(error);
        })
    })
}