// Krabi Reisgids: bundelt private/gids.json + private/tips.json en versleutelt met AES-256-GCM (PBKDF2-SHA256, 310000 iteraties).
// Gebruik: node encrypt.js private/gids.json private/tips.json data/gids.enc .password
const fs=require('fs'),crypto=require('crypto');
const [,,gidsF,tipsF,outF,pwF]=process.argv;
if(!gidsF||!tipsF||!outF||!pwF){console.error('Gebruik: node encrypt.js <gids.json> <tips.json> <uit.enc> <.password>');process.exit(1);}
const pw=fs.readFileSync(pwF,'utf8').trim();
if(pw.length<8){console.error("Wachtwoord te kort (min. 8 tekens)");process.exit(1);}
const gids=JSON.parse(fs.readFileSync(gidsF,'utf8'));
const tips=fs.existsSync(tipsF)?JSON.parse(fs.readFileSync(tipsF,'utf8')):{tips:[]};
const okUrl=u=>!u||/^https?:\/\//i.test(u);
for(const t of (tips.tips||[])){if(!t.section||!t.text){console.error('Tip zonder section/text:',JSON.stringify(t));process.exit(1);}if(!okUrl(t.url)){console.error('Ongeldige URL in tip:',t.url);process.exit(1);}}
const payload=Buffer.from(JSON.stringify({updated:new Date().toISOString(),gids,tips:tips.tips||[]}));
const salt=crypto.randomBytes(16),iv=crypto.randomBytes(12),iter=310000;
const key=crypto.pbkdf2Sync(pw,salt,iter,32,'sha256');
const c=crypto.createCipheriv('aes-256-gcm',key,iv);
const ct=Buffer.concat([c.update(payload),c.final(),c.getAuthTag()]);
fs.writeFileSync(outF,JSON.stringify({v:1,kdf:'PBKDF2-SHA256',iter,salt:salt.toString('base64'),iv:iv.toString('base64'),ct:ct.toString('base64')}));
console.log(`Versleuteld: ${(gids.sections||[]).length} onderdelen, ${(tips.tips||[]).length} tips -> ${outF}`);
