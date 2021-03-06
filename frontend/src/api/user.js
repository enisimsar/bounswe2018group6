import request from '@/utils/request'
import { getToken } from '@/utils/auth' // getToken from cookie

export function loginByUsername(username, password) {
  const data = {
    username,
    password
  }
  return request({
    url: '/auth/',
    method: 'post',
    data
  })
}

export function getUserInfo(user_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/user/' + user_id + '/',
    method: 'get'
  })
}

export function signupDate(first_name, last_name, email, username, password) {
  const data = {
    first_name,
    last_name,
    email,
    username,
    password
  }
  return request({
    url: '/signup/',
    method: 'post',
    data
  })
}

export function editUser(user_id, data) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/user/' + user_id + '/',
    method: 'put',
    data
  })
}

export function follow(object_id) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  const data = {
    "content_type": "user",
    "object_id": object_id
  }
  return request({
    headers,
    url: '/follow/',
    method: 'post',
    data
  })
}

export function userSearch(username) {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/users_list/?search=' + username,
    method: 'get'
  })
}

export function getAllNotifications() {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/notifications/all/',
    method: 'get'
  })
}

export function getUnreadNotifications() {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/notifications/unread/',
    method: 'get'
  })
}

export function makeNotificationsRead() {
  const headers = {
    //ContentType: 'application/json',
    Authorization: 'Token ' + getToken(),
  }
  return request({
    headers,
    url: '/notifications/mark_as_read/',
    method: 'post'
  })
}
