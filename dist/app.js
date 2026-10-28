const menuButton=document.querySelector('.menu-toggle');
const mobileMenu=document.querySelector('#mobile-menu');
menuButton.addEventListener('click',()=>{const expanded=menuButton.getAttribute('aria-expanded')==='true';menuButton.setAttribute('aria-expanded',String(!expanded));mobileMenu.hidden=expanded;menuButton.querySelector('.menu-label').textContent=expanded?'Menu':'Close';});
document.querySelectorAll('.nav-dropdown>button').forEach(button=>{
  button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')==='true';closeDropdowns();button.setAttribute('aria-expanded',String(!open));document.getElementById(button.getAttribute('aria-controls')).hidden=open;});
});
function closeDropdowns(){document.querySelectorAll('.nav-dropdown>button').forEach(b=>{b.setAttribute('aria-expanded','false');document.getElementById(b.getAttribute('aria-controls')).hidden=true;});}
document.addEventListener('click',event=>{if(!event.target.closest('.nav-dropdown'))closeDropdowns();});
document.addEventListener('keydown',event=>{if(event.key==='Escape'){const active=document.querySelector('.nav-dropdown>button[aria-expanded=true]');closeDropdowns();if(active)active.focus();if(!mobileMenu.hidden){mobileMenu.hidden=true;menuButton.setAttribute('aria-expanded','false');menuButton.querySelector('.menu-label').textContent='Menu';menuButton.focus();}}});
document.querySelectorAll('.mobile-panel a').forEach(a=>a.addEventListener('click',()=>{mobileMenu.hidden=true;menuButton.setAttribute('aria-expanded','false');menuButton.querySelector('.menu-label').textContent='Menu';}));
document.querySelectorAll('.service-toggle').forEach(button=>{
  button.addEventListener('click',()=>{
    const wasOpen=button.getAttribute('aria-expanded')==='true';
    document.querySelectorAll('.service-toggle').forEach(b=>{b.setAttribute('aria-expanded','false');b.querySelector('.plus').textContent='+';document.getElementById(b.getAttribute('aria-controls')).hidden=true;});
    if(!wasOpen){button.setAttribute('aria-expanded','true');button.querySelector('.plus').textContent='−';document.getElementById(button.getAttribute('aria-controls')).hidden=false;document.querySelector('#service-photo').src=button.dataset.image;document.querySelector('#service-photo').alt=button.dataset.alt;document.querySelector('#service-caption').textContent=button.querySelector('.name').textContent;document.querySelector('#service-index').textContent=button.dataset.number+' / 02';}
  });
});
const slides=[...document.querySelectorAll('.testimonial-slide')];let activeTestimonial=0;
const feedbackCount=document.querySelector('#feedback-current');
function showTestimonial(index){activeTestimonial=(index+slides.length)%slides.length;slides.forEach((slide,i)=>slide.hidden=i!==activeTestimonial);feedbackCount.textContent=String(activeTestimonial+1).padStart(2,'0');}
if(slides.length){
document.querySelector('#feedback-next').addEventListener('click',()=>showTestimonial(activeTestimonial+1));
document.querySelector('#feedback-prev').addEventListener('click',()=>showTestimonial(activeTestimonial-1));
document.querySelector('.all-feedback-toggle').addEventListener('click',event=>{
 const all=event.currentTarget.getAttribute('aria-expanded')!=='true';event.currentTarget.setAttribute('aria-expanded',String(all));event.currentTarget.textContent=all?'Show one at a time':'Read all feedback';document.querySelector('.feedback-slides').classList.toggle('show-all',all);slides.forEach((s,i)=>s.hidden=!all&&i!==activeTestimonial);document.querySelectorAll('.feedback-controls button').forEach(b=>b.disabled=all);
});
}
const clients=document.querySelector('.client-track');
if(clients){
const clientSection=document.querySelector('.clients');
const reduceMotion=matchMedia('(prefers-reduced-motion: reduce)');
const originalClientLogos=[...clients.children];
originalClientLogos.forEach(logo=>{const copy=logo.cloneNode(true);copy.setAttribute('aria-hidden','true');copy.classList.add('client-logo-copy');copy.querySelector('img').alt='';clients.append(copy);});
const pauseClients=document.createElement('button');
pauseClients.type='button';pauseClients.id='clients-pause';pauseClients.className='round-button';
document.querySelector('.client-controls').prepend(pauseClients);
let clientPaused=reduceMotion.matches,clientVisible=false,clientResumeAt=0,lastClientFrame=0,clientPosition=clients.scrollLeft;
function updateClientPause(){pauseClients.setAttribute('aria-label',clientPaused?'Play client logo animation':'Pause client logo animation');pauseClients.setAttribute('aria-pressed',String(clientPaused));pauseClients.innerHTML=clientPaused?'<svg class="arrow" viewBox="0 0 20 20" aria-hidden="true"><path d="m7 4 9 6-9 6z"/></svg>':'<svg class="arrow" viewBox="0 0 20 20" aria-hidden="true"><path d="M7 4v12M13 4v12"/></svg>';}
updateClientPause();pauseClients.addEventListener('click',()=>{clientPaused=!clientPaused;updateClientPause();});
clients.addEventListener('touchstart',()=>clientResumeAt=performance.now()+6000,{passive:true});
clients.addEventListener('wheel',()=>clientResumeAt=performance.now()+4000,{passive:true});
reduceMotion.addEventListener('change',event=>{clientPaused=event.matches;updateClientPause();});
new IntersectionObserver(entries=>{clientVisible=entries[0].isIntersecting;},{threshold:0.05}).observe(clientSection);
function clientLoopWidth(){return clients.children[originalClientLogos.length].offsetLeft-originalClientLogos[0].offsetLeft;}
function moveClients(direction){
 const loop=clientLoopWidth();clientResumeAt=performance.now()+1600;
 if(direction<0&&clients.scrollLeft<clients.clientWidth*.8)clients.scrollLeft+=loop;
 if(direction>0&&clients.scrollLeft>=loop)clients.scrollLeft-=loop;
 clients.scrollBy({left:direction*clients.clientWidth*.8,behavior:reduceMotion.matches?'instant':'smooth'});
}
document.querySelector('#clients-next').addEventListener('click',()=>moveClients(1));
document.querySelector('#clients-prev').addEventListener('click',()=>moveClients(-1));
function animateClients(now){
 const delta=Math.min(now-(lastClientFrame||now),50);lastClientFrame=now;
 if(clientVisible&&!document.hidden&&!clientPaused&&now>clientResumeAt){
  const loop=clientLoopWidth();
  // Accumulate sub-pixel movement independently of rounded browser scroll positions.
  clientPosition+=delta*.04;
  if(loop>0&&clientPosition>=loop)clientPosition%=loop;
  clients.scrollLeft=clientPosition;
 }else{clientPosition=clients.scrollLeft;}
 requestAnimationFrame(animateClients);
}
requestAnimationFrame(animateClients);
}
