export type Stat={seen:number;correct:number;wrong:number;streakCorrect:number};
export type Progress={name:string;topic:number|null;xp:number;correct:number;wrong:number;streak:number;maxStreak:number;stats:Record<string,Stat>;phase:number;completedTopics:number[];achievements:string[];sound:boolean;startedAt:number;lastSession:number};
export const initialProgress:Progress={name:'',topic:null,xp:0,correct:0,wrong:0,streak:0,maxStreak:0,stats:{},phase:0,completedTopics:[],achievements:[],sound:true,startedAt:Date.now(),lastSession:Date.now()};
export const levels=[['Visitante',0],['Explorador',1000],['Investigador',2500],['Arqueólogo',5000],['Guardião da Memória',9000]] as const;
