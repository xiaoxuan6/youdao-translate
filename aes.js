const crypto = require('crypto')

function T(e) {
    return crypto.createHash("md5").update(e).digest()
}


function dec(e, t, o) {
    if (!e)
        return null;
    const a = Buffer.alloc(16, T(t))
        , n = Buffer.alloc(16, T(o))
        , r = crypto.createDecipheriv("aes-128-cbc", a, n);
    let l = r.update(e, "base64", "utf-8");
    return l += r.final("utf-8"),
        l
}
