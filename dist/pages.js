// Programme categories retain the full source lists; filters reveal each category.
const filterButtons=[...document.querySelectorAll('[data-filter]')];
filterButtons.forEach(button=>button.addEventListener('click',()=>{
 const chosen=button.dataset.filter;
 filterButtons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 let count=0;document.querySelectorAll('[data-category]').forEach(card=>{card.hidden=chosen!=='all'&&card.dataset.category!==chosen;if(!card.hidden)count++;});
 document.querySelector('.filter-count').textContent=count===1?'1 programme category':`${count} programme categories`;
}));

// A native dialog provides full-image viewing, keyboard navigation and focus return.
const imageDialog=document.querySelector('.media-dialog');
let lightboxItems=[],lightboxIndex=0,lightboxOpener=null;
function showLightbox(index){
 lightboxIndex=(index+lightboxItems.length)%lightboxItems.length;
 const item=lightboxItems[lightboxIndex];const image=document.querySelector('#lightbox-image');image.src=item.src;image.alt=item.caption;
 document.querySelector('#lightbox-caption').textContent=item.caption;
 document.querySelector('.dialog-counter').textContent=`${String(lightboxIndex+1).padStart(2,'0')} / ${String(lightboxItems.length).padStart(2,'0')}`;
 document.querySelector('.dialog-prev').hidden=lightboxItems.length===1;document.querySelector('.dialog-next').hidden=lightboxItems.length===1;
}
document.querySelectorAll('[data-lightbox]').forEach(button=>button.addEventListener('click',()=>{
 lightboxOpener=button;
 if(button.dataset.lightbox==='profile'){
  lightboxItems=[...document.querySelectorAll('[data-profile-src]')].map((b,i)=>({src:b.dataset.profileSrc,caption:`Company Profile · Page ${i+1} of 13`}));
  lightboxIndex=Number(document.querySelector('#profile-select').value);
 }else{
  const group=[...document.querySelectorAll('[data-lightbox]')].filter(b=>b.dataset.lightbox===button.dataset.lightbox);
  lightboxItems=group.map(b=>({src:b.querySelector('img').src,caption:b.dataset.caption}));lightboxIndex=group.indexOf(button);
 }
 showLightbox(lightboxIndex);imageDialog.showModal();document.body.style.overflow='hidden';
}));
if(imageDialog){
 const closeDialog=()=>imageDialog.close();
 imageDialog.querySelector('.dialog-close').addEventListener('click',closeDialog);
 imageDialog.querySelector('.dialog-prev').addEventListener('click',()=>showLightbox(lightboxIndex-1));
 imageDialog.querySelector('.dialog-next').addEventListener('click',()=>showLightbox(lightboxIndex+1));
 imageDialog.addEventListener('keydown',event=>{if(event.key==='ArrowRight'){event.preventDefault();showLightbox(lightboxIndex+1);}if(event.key==='ArrowLeft'){event.preventDefault();showLightbox(lightboxIndex-1);}});
 imageDialog.addEventListener('click',event=>{if(event.target===imageDialog)closeDialog();});
 imageDialog.addEventListener('close',()=>{document.body.style.overflow='';lightboxOpener?.focus();});
}

const profileSelect=document.querySelector('#profile-select');
if(profileSelect){
 const thumbnails=[...document.querySelectorAll('[data-profile-page]')];
 function showProfile(index){
  index=Math.max(0,Math.min(thumbnails.length-1,index));profileSelect.value=String(index);
  const image=document.querySelector('#profile-image');image.src=thumbnails[index].dataset.profileSrc;image.alt=`ShyanaHR company profile — page ${index+1}`;
  document.querySelector('.profile-large').dataset.caption=`Company Profile · Page ${index+1} of 13`;
  thumbnails.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
  document.querySelector('#profile-prev').disabled=index===0;document.querySelector('#profile-next').disabled=index===thumbnails.length-1;
 }
 thumbnails.forEach((button,index)=>button.addEventListener('click',()=>showProfile(index)));
 profileSelect.addEventListener('change',()=>showProfile(Number(profileSelect.value)));
 document.querySelector('#profile-prev').addEventListener('click',()=>showProfile(Number(profileSelect.value)-1));
 document.querySelector('#profile-next').addEventListener('click',()=>showProfile(Number(profileSelect.value)+1));showProfile(0);
}

const enquiryForm=document.querySelector('#enquiry-form');
if(enquiryForm){
 const selectedInterest=new URLSearchParams(location.search).get('interest');
 enquiryForm.querySelectorAll('[name="area_interest"]').forEach(input=>{if(input.value===selectedInterest)input.checked=true;});
 enquiryForm.addEventListener('submit',event=>{
  event.preventDefault();if(!enquiryForm.reportValidity())return;
  const form=new FormData(enquiryForm);
  const labels=[['company_name','Company Name'],['no_of_employees','No of Employees'],['name','Name'],['email','Email'],['job_title','Job Title'],['contact','Phone Number'],['zip_code','Zip Code']];
  const lines=labels.map(([key,label])=>`${label}: ${form.get(key)||'—'}`);
  lines.push('',`Area(s) of Interest: ${form.getAll('area_interest').join(', ')||'—'}`,'','Message:',String(form.get('message')),'',`How did you hear about SCT?: ${form.getAll('source').join(', ')||'—'}`);
  const text=lines.join('\n');const preview=document.querySelector('#enquiry-preview');
  document.querySelector('#enquiry-text').textContent=text;
  document.querySelector('#enquiry-send').href=`mailto:support@shyanahr.com.my?subject=${encodeURIComponent('Website enquiry — '+form.get('name'))}&body=${encodeURIComponent(text)}`;
  preview.hidden=false;preview.focus();
  document.querySelector('#enquiry-download').onclick=()=>{const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const link=document.createElement('a');link.href=url;link.download='ShyanaHR-enquiry.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
 });
}
