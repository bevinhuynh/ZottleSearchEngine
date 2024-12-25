import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import HomePage from './HomePage.tsx'
import SearchPage from './pages/SearchPage.tsx'
import {createBrowserRouter, RouterProvider} from 'react-router-dom';

if (!localStorage.getItem('currentTheme')) {
  localStorage.setItem('darkMode', "Dark Mode");
  localStorage.setItem('darkColor', '#3f3f3f');
  localStorage.setItem('lightMode', 'Light Mode')
  localStorage.setItem('lightColor', '#ffffff')
  localStorage.setItem('currentTheme', 'darkMode')
  const darkColor = localStorage.getItem('darkColor');
  if (darkColor) {
    document.body.style.backgroundColor = darkColor;
  }
  console.log("Initialized both themes in local storage");
}

const currentTheme = localStorage.getItem('currentTheme');
let current_mode = document.getElementById("footer-content");
let github = document.getElementById("github-link");
let about = document.getElementById("about-link");
if (currentTheme == 'darkMode') {
    const darkColor = localStorage.getItem('darkColor');
    if (darkColor) {
      document.body.style.background = darkColor;
    }   
}
else {
  const lightColor = localStorage.getItem('lightColor');
  if (lightColor) {
      document.body.style.background = lightColor;
  }
}


  if (currentTheme == 'darkMode') {
    if (github && about) {
      github.style.color = 'black';
      about.style.color = 'black';
    }
    if (current_mode) {
      console.log('yes');
      current_mode.innerHTML = "Light Mode";
    }
  }





const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage/>
  },
  {
    path:'/search',
    element: <SearchPage/>
  }
    
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router}/>
  </StrictMode>,
)
