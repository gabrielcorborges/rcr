import {topics} from './topics';
export type Question={id:string;topic:number;type:'choice'|'truth'|'complete'|'identify';category:string;prompt:string;options:string[];answer:string;explanation:string};
const distract=['Uma certeza universal','Uma cidade moderna','Um documento escrito'];
export const questions:Question[]=topics.flatMap(t=>{
 const source=t.slidesData.flatMap(s=>s.keys.map((k,i)=>({s,k,i})));
 const facts=Array.from({length:30},(_,i)=>source[i%source.length]);
 return facts.map((f,i)=>{
  const type=(['choice','truth','complete','identify'] as const)[i%4];
  const id=`t${t.id}-${i+1}`; const angle=['conceito','fala','vestígio'][Math.floor(i/source.length)]||'memória'; const cat=f.k.split(' / ')[0];
  if(type==='truth') return {id,topic:t.id,type,category:cat,prompt:`Na trilha de ${angle}: “${f.k}” faz parte das pistas essenciais de “${f.s.title}”.`,options:['Verdade','Armadilha'],answer:'Verdade',explanation:`Verdade. ${f.s.text}`};
  if(type==='complete') return {id,topic:t.id,type,category:cat,prompt:`Complete a fala (${angle}): “Ao explicar ${f.s.title}, preciso lembrar de ____.”`,options:[f.k,...distract.slice(0,3)],answer:f.k,explanation:`A pista é “${f.k}”. ${f.s.text}`};
  if(type==='identify') return {id,topic:t.id,type,category:cat,prompt:`Pensando em ${angle}, qual pista ajuda a identificar o slide “${f.s.title}”?`,options:[f.k,...distract],answer:f.k,explanation:`${f.k} se conecta diretamente ao slide. ${f.s.text}`};
  return {id,topic:t.id,type,category:cat,prompt:`Na perspectiva de ${angle}, que ideia pertence a “${f.s.title}”?`,options:[f.k,...distract],answer:f.k,explanation:f.s.text};
 });
});
export const questionCount=questions.length;
