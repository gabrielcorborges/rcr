import {useEffect,useState} from 'react';import {initialProgress,Progress} from '../data/progress';
const KEY='ecos-da-pedra-progress-v1';
export function useProgress(){const [p,setP]=useState<Progress>(()=>{try{return {...initialProgress,...JSON.parse(localStorage.getItem(KEY)||'{}')}}catch{return initialProgress}});useEffect(()=>localStorage.setItem(KEY,JSON.stringify({...p,lastSession:Date.now()})),[p]);return {p,setP,reset:()=>{localStorage.removeItem(KEY);setP({...initialProgress,startedAt:Date.now()})}}}
