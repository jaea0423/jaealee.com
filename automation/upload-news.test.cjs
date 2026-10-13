const test=require('node:test'),assert=require('node:assert/strict');
const {interpret,redact,configQuote}=require('./upload-news.cjs');
test('requires successful HTTP, ok:true and the requested date',()=>{
 assert.deepEqual(interpret('{"ok":true,"date":"2026-10-13"}',200,'2026-10-13'),{ok:true});
 assert.equal(interpret('{"ok":true,"date":"2026-10-12"}',200,'2026-10-13').ok,false);
 assert.equal(interpret('{"ok":true,"date":"2026-10-13"}',500,'2026-10-13').ok,false);
});
test('server errors cannot echo credentials into results',()=>{
 const r=interpret('{"message":"bad secret-token"}',401,'2026-10-13',['secret-token']);assert(!r.error.includes('secret-token'));assert(r.error.includes('[REDACTED]'));
 assert.equal(redact('secret-token key',['secret-token','key']),'[REDACTED] [REDACTED]');
});
test('rejects header injection in curl config',()=>{assert.throws(()=>configQuote('key\nheader=malicious'));});
