import {RouteRecordRaw} from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayoutPost.vue'),
    children: [
      {path: '', component: () => import('pages/IndexPage.vue')}
    ]

  },
  {
    path: '/403',
    name: '403',
    component: () => import('pages/Error403.vue')
  },

  {
    path: '/post',
    meta: {isAllowBack: true},
    component: () => import('layouts/MainLayoutPost.vue'),
    children: [
      {path: 'add', component: () => import('pages/post/post_add.vue')},
      {path: 'view', component: () => import('pages/post/post_view.vue')},
      {path: 'list', component: () => import('pages/post/post_list.vue')},
      {path: 'list/:catid', component: () => import('pages/post/post_list.vue')},
      {path: 'listp/:pid', component: () => import('pages/post/post_list.vue')},
      {path: 'edit', component: () => import('pages/post/post_edit.vue')},
    ],
  },

  {
    path: '/userinfo',
    meta: {isAllowBack: true, needLogin: true},
    component: () => import('layouts/MainLayoutUser.vue'),
    children: [
      {path: 'register', component: () => import('pages/user/user_register.vue')},
      {path: 'login', component: () => import('pages/user/user_login.vue')},
      {path: 'info', component: () => import('pages/user/user_info.vue')},
      {path: 'changerole', component: () => import('pages/user/user_changerole.vue')},
      {path: 'changepass', component: () => import('pages/user/user_changepass.vue')},
      {path: 'changeinfo', component: () => import('pages/user/user_changeinfo.vue')},


    ],
  },


  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
