(() => {
 const preference=matchMedia('(prefers-reduced-motion: reduce)');
 if(preference.matches||!('IntersectionObserver' in window))return;
 document.documentElement.classList.add('motion-enabled');

 // Reveal the existing headline word by word, retaining its text and semantics.
 const title=document.querySelector('main h1');
 if(title){
  title.setAttribute('aria-label',title.innerText.replace(/\s+/g,' ').trim());
  const walker=document.createTreeWalker(title,NodeFilter.SHOW_TEXT);
  const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
  let order=0;
  nodes.forEach(node=>{
   if(!node.textContent.trim())return;
   const fragment=document.createDocumentFragment();
   node.textContent.split(/(\s+)/).forEach(word=>{
    if(!word.trim()){fragment.append(document.createTextNode(word));return;}
    const wrap=document.createElement('span');wrap.className='motion-word-wrap';wrap.setAttribute('aria-hidden','true');
    const inner=document.createElement('span');inner.className='motion-word';inner.style.setProperty('--word-order',String(order++));inner.textContent=word;
    wrap.append(inner);fragment.append(wrap);
   });
   node.replaceWith(fragment);
  });
  title.classList.add('entrance-title');
 }

 const targets=document.querySelectorAll('.section-head,.feedback-intro,.feedback-slides,.different>div,.programme,.consulting-card,.development-card,.media-grid figure,.about-principles article,.about-team-copy,.value-item,.core-description,.service-contact>div,.contact-side,.form-field,fieldset,.profile-toolbar,.profile-stage,.profile-thumbnails,.footer-cta,.footer-columns>*,.footer-quotes h3,.wisdom,main h2');
 targets.forEach(element=>{
  if(element.parentElement.closest('[data-reveal]'))return;
  element.dataset.reveal='section';
  const siblings=[...element.parentElement.children];
  if(element.matches('.programme,.consulting-card,.media-grid figure,.value-item,.wisdom'))element.style.setProperty('--reveal-delay',`${(siblings.indexOf(element)%3)*85}ms`);
 });
 document.querySelectorAll('.hero-media,.page-wide-photo,.service-image,.different-visual').forEach(element=>{element.dataset.reveal='image';});
 const observer=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
   if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target);}
  });
 },{threshold:0,rootMargin:'0px 0px -28px 0px'});
 document.querySelectorAll('[data-reveal]').forEach(element=>observer.observe(element));

 // Count up only on first view; keep the final value available to assistive tech.
 const counters=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
   if(!entry.isIntersecting)return;
   const element=entry.target;const total=Number(element.textContent);const start=performance.now();
   element.setAttribute('aria-label',String(total));
   function count(now){
    if(preference.matches){element.textContent=String(total);return;}
    const progress=Math.min((now-start)/1100,1);element.textContent=String(Math.round(total*(1-Math.pow(1-progress,3))));
    if(progress<1)requestAnimationFrame(count);
   }
   requestAnimationFrame(count);counters.unobserve(element);
  });
 },{threshold:.5});
 document.querySelectorAll('.metric strong').forEach(element=>counters.observe(element));

 const photos=[...document.querySelectorAll('.hero-media,.page-wide-photo,.different-visual')];
 photos.forEach(element=>element.classList.add('motion-photo'));
 const header=document.querySelector('.site-header');let pending=false;
 function updateScroll(){
  pending=false;header?.classList.toggle('header-scrolled',scrollY>20);
  if(preference.matches)return;
  photos.forEach(element=>{
   const rect=element.getBoundingClientRect();
   if(rect.bottom<0||rect.top>innerHeight)return;
   const offset=Math.max(-12,Math.min(12,((innerHeight/2-rect.top-rect.height/2)/innerHeight)*22));
   element.style.setProperty('--photo-offset',`${offset.toFixed(2)}px`);
  });
 }
 addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(updateScroll);}},{passive:true});
 addEventListener('resize',updateScroll);updateScroll();
 // Filtering may reveal an offscreen item immediately; do not leave it transparent.
 document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('.development-card:not([hidden])').forEach(card=>card.classList.add('is-visible'));
 }));
 preference.addEventListener('change',event=>{
  if(event.matches){document.documentElement.classList.remove('motion-enabled');observer.disconnect();counters.disconnect();document.querySelectorAll('[data-reveal]').forEach(el=>el.classList.add('is-visible'));}
 });
})();
