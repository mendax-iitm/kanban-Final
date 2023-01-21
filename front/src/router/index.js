import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginForm from "../components/LoginForm.vue";
import RegisterForm from "../components/Register.vue";
import TestingAPI from "../components/Test.vue";
import AddCard from "../components/AddCard.vue";
import EditCard from "../components/EditCard.vue";
import AddList from "../components/AddList.vue";
import Summary from "../components/Summary.vue";
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginForm,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterForm,
  },
  {
    path: "/test",
    name: "test",
    component: TestingAPI,
  },
  {
    path: "/addCard/:id",
    name: "addCard",
    component: AddCard,
  },
  {
    path: "/addList",
    name: "addList",
    component: AddList,
  },
  {
    path: "/editCard/:id",
    name: "editCard",
    component: EditCard,
  },
  { path: "/summary", name: "summary", component: Summary },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
];

const router = new VueRouter({
  routes,
});

export default router;
