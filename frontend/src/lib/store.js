/**
 * 스토어 변수 생성하기
 *
 * 그리고
 * 지속성 스토어 - persistent store
 *
 */
import { writable } from 'svelte/store';

const persist_storage = (key, initValue) => {
  const storedValueStr = localStorage.getItem(key);
  const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue);
  store.subscribe(val => {
    localStorage.setItem(key, JSON.stringify(val));
  });
  return store;
};

export const page = persist_storage('page', 0)
export const access_token = persist_storage('access_token', "")  // 로그인 정보 
export const username = persist_storage("username","")
export const is_login = persist_storage("is_login", false)
export const keyword = persist_storage("keyword", "")