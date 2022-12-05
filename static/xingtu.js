// 逆向星图sign参数
// 测试参数
text_args = "limit10page1queryqueryservice_methodDemanderGetUniversalDemandListservice_nametask.AdStarTaskServicesign_strict1e39539b8836fb99e1538974d3ac1fe98"
// text_args = "service_methodStarDemanderBasicInfoservice_namedemander.AdStarDemanderServicesign_strict1e39539b8836fb99e1538974d3ac1fe98"
n = undefined

window = global
rotl = function (e, t) {
    return e << t | e >>> 32 - t
}
endian = function (e) {
    if (e.constructor == Number) {
        return 16711935 & rotl(e, 8) | 4278255360 & rotl(e, 24)
    }
    for (var t = 0; t < e.length; t++) {
        e[t] = endian(e[t])
    }
    return e
}
var t = {
    utf8: {
        stringToBytes: function (e) {
            return t.bin.stringToBytes(unescape(encodeURIComponent(e)))
        },
        bytesToString: function (e) {
            return decodeURIComponent(escape(t.bin.bytesToString(e)))
        }
    },
    bin: {
        stringToBytes: function (e) {
            for (var t = [], n = 0; n < e.length; n++) {
                t.push(255 & e.charCodeAt(n))
            }
            return t
        },
        bytesToString: function (e) {
            for (var t = [], n = 0; n < e.length; n++) {
                t.push(String.fromCharCode(e[n]))
            }
            return t.join("")
        }
    },
    bytesToWords: function (e) {
        for (var t = [], n = 0, r = 0; n < e.length; n++,
            r += 8) {
            t[r >>> 5] |= e[n] << 24 - r % 32
        }
        return t
    },
    wordsToBytes: function (e) {
        for (var t = [], n = 0; n < 32 * e.length; n += 8) {
            t.push(e[n >>> 5] >>> 24 - n % 32 & 255)
        }
        return t
    },
    bytesToHex: function (e) {
        for (var t = [], n = 0; n < e.length; n++) {
            t.push((e[n] >>> 4).toString(16)),
                t.push((15 & e[n]).toString(16))
        }
        return t.join("")
    }

}
var r = {
    stringToBytes: function (e) {
        return t.bin.stringToBytes(unescape(encodeURIComponent(e)))
    },

}
a._hh = function (e, t, n, r, i, o, a) {
    var s = e + (t ^ n ^ r) + (i >>> 0) + a;
    return (s << o | s >>> 32 - o) + t
}
a._ff = function (e, t, n, r, i, o, a) {
    var s = e + (t & n | ~t & r) + (i >>> 0) + a;
    return (s << o | s >>> 32 - o) + t
}
a._gg = function (e, t, n, r, i, o, a) {
    var s = e + (t & r | n & ~r) + (i >>> 0) + a;
    return (s << o | s >>> 32 - o) + t
}
a._ii = function (e, t, n, r, i, o, a) {
    var s = e + (n ^ (t | ~r)) + (i >>> 0) + a;
    return (s << o | s >>> 32 - o) + t
}


function a(e, n) {
    e.constructor == String ? e = n && "binary" === n.encoding ? o.stringToBytes(e) : r.stringToBytes(e) : i(e) ? e = Array.prototype.slice.call(e, 0) : Array.isArray(e) || e.constructor === Uint8Array || (e = e.toString());
    for (var s = t.bytesToWords(e), l = 8 * e.length, c = 1732584193, u = -271733879, d = -1732584194, f = 271733878, h = 0; h < s.length; h++) {
        s[h] = 16711935 & (s[h] << 8 | s[h] >>> 24) | 4278255360 & (s[h] << 24 | s[h] >>> 8)
    }
    s[l >>> 5] |= 128 << l % 32, s[14 + (l + 64 >>> 9 << 4)] = l;
    var p = a._ff, m = a._gg, g = a._hh, v = a._ii;
    for (h = 0; h < s.length; h += 16) {
        var y = c, A = u, b = d, _ = f;
        c = p(c, u, d, f, s[h + 0], 7, -680876936), f = p(f, c, u, d, s[h + 1], 12, -389564586), d = p(d, f, c, u, s[h + 2], 17, 606105819), u = p(u, d, f, c, s[h + 3], 22, -1044525330), c = p(c, u, d, f, s[h + 4], 7, -176418897), f = p(f, c, u, d, s[h + 5], 12, 1200080426), d = p(d, f, c, u, s[h + 6], 17, -1473231341), u = p(u, d, f, c, s[h + 7], 22, -45705983), c = p(c, u, d, f, s[h + 8], 7, 1770035416), f = p(f, c, u, d, s[h + 9], 12, -1958414417), d = p(d, f, c, u, s[h + 10], 17, -42063), u = p(u, d, f, c, s[h + 11], 22, -1990404162), c = p(c, u, d, f, s[h + 12], 7, 1804603682), f = p(f, c, u, d, s[h + 13], 12, -40341101), d = p(d, f, c, u, s[h + 14], 17, -1502002290), u = p(u, d, f, c, s[h + 15], 22, 1236535329), c = m(c, u, d, f, s[h + 1], 5, -165796510), f = m(f, c, u, d, s[h + 6], 9, -1069501632), d = m(d, f, c, u, s[h + 11], 14, 643717713), u = m(u, d, f, c, s[h + 0], 20, -373897302), c = m(c, u, d, f, s[h + 5], 5, -701558691), f = m(f, c, u, d, s[h + 10], 9, 38016083), d = m(d, f, c, u, s[h + 15], 14, -660478335), u = m(u, d, f, c, s[h + 4], 20, -405537848), c = m(c, u, d, f, s[h + 9], 5, 568446438), f = m(f, c, u, d, s[h + 14], 9, -1019803690), d = m(d, f, c, u, s[h + 3], 14, -187363961), u = m(u, d, f, c, s[h + 8], 20, 1163531501), c = m(c, u, d, f, s[h + 13], 5, -1444681467), f = m(f, c, u, d, s[h + 2], 9, -51403784), d = m(d, f, c, u, s[h + 7], 14, 1735328473), u = m(u, d, f, c, s[h + 12], 20, -1926607734), c = g(c, u, d, f, s[h + 5], 4, -378558), f = g(f, c, u, d, s[h + 8], 11, -2022574463), d = g(d, f, c, u, s[h + 11], 16, 1839030562), u = g(u, d, f, c, s[h + 14], 23, -35309556), c = g(c, u, d, f, s[h + 1], 4, -1530992060), f = g(f, c, u, d, s[h + 4], 11, 1272893353), d = g(d, f, c, u, s[h + 7], 16, -155497632), u = g(u, d, f, c, s[h + 10], 23, -1094730640), c = g(c, u, d, f, s[h + 13], 4, 681279174), f = g(f, c, u, d, s[h + 0], 11, -358537222), d = g(d, f, c, u, s[h + 3], 16, -722521979), u = g(u, d, f, c, s[h + 6], 23, 76029189), c = g(c, u, d, f, s[h + 9], 4, -640364487), f = g(f, c, u, d, s[h + 12], 11, -421815835), d = g(d, f, c, u, s[h + 15], 16, 530742520), u = g(u, d, f, c, s[h + 2], 23, -995338651), c = v(c, u, d, f, s[h + 0], 6, -198630844), f = v(f, c, u, d, s[h + 7], 10, 1126891415), d = v(d, f, c, u, s[h + 14], 15, -1416354905), u = v(u, d, f, c, s[h + 5], 21, -57434055), c = v(c, u, d, f, s[h + 12], 6, 1700485571), f = v(f, c, u, d, s[h + 3], 10, -1894986606), d = v(d, f, c, u, s[h + 10], 15, -1051523), u = v(u, d, f, c, s[h + 1], 21, -2054922799), c = v(c, u, d, f, s[h + 8], 6, 1873313359), f = v(f, c, u, d, s[h + 15], 10, -30611744), d = v(d, f, c, u, s[h + 6], 15, -1560198380), u = v(u, d, f, c, s[h + 13], 21, 1309151649), c = v(c, u, d, f, s[h + 4], 6, -145523070), f = v(f, c, u, d, s[h + 11], 10, -1120210379), d = v(d, f, c, u, s[h + 2], 15, 718787259), u = v(u, d, f, c, s[h + 9], 21, -343485551), c = c + y >>> 0, u = u + A >>> 0, d = d + b >>> 0, f = f + _ >>> 0
    }
    return endian([c, u, d, f])
}

function get_sign1(page) {
    text_args = "limit10page" + page + "queryqueryservice_methodDemanderGetUniversalDemandListservice_nametask.AdStarTaskServicesign_strict1e39539b8836fb99e1538974d3ac1fe98"
    n = undefined
    result = t.bytesToHex(t.wordsToBytes(a(text_args, n)))
    return result
}

function get_sign2(challenge_id) {
    text_args = "challenge_id" + challenge_id + "service_methodDemanderGetChallengeservice_namechallenge.AdStarChallengeServicesign_strict1e39539b8836fb99e1538974d3ac1fe98"
    n = undefined
    result = t.bytesToHex(t.wordsToBytes(a(text_args, n)))
    return result
}

// 搜索关键词的调用
function search_key(key) {
    text_args = "attribute_filterattribute_filterauthor_list_filterauthor_list_filterauthor_pack_filterauthor_pack_filterdisplay_scene1key" + key + "limit20order_byscorepage1platform_source1regular_filterregular_filtersearch_scene1service_methodSearchForStarAuthorsservice_namego_search.AdStarGoSearchServicesign_strict1sort_type2e39539b8836fb99e1538974d3ac1fe98"
    n = undefined
    result = t.bytesToHex(t.wordsToBytes(a(text_args, n)))
    return result
}

// 获取粉丝覆盖情况
function shoping(star_id) {
    star_id = star_id + ""
    text_args = "o_author_id" + star_id + "platform_channel1platform_source1range2service_methodGetAuthorShoppingInfoservice_namedata_space.AdStarDataSpaceServicesign_strict1e39539b8836fb99e1538974d3ac1fe98"
    console.log(text_args)
    n = undefined
    result = t.bytesToHex(t.wordsToBytes(a(text_args, n)))
    return result
}

// 报价服务
function authorService(star_id) {
    star_id = star_id + ""
    text_args = "o_author_id"+star_id+"platform_channel1platform_source1service_methodGetAuthorMarketingInfoservice_nameauthor.AdStarAuthorServicesign_strict1e39539b8836fb99e1538974d3ac1fe98"
    n = undefined
    result = t.bytesToHex(t.wordsToBytes(a(text_args, n)))
    return result
}
// 星图指数
function authorLinkSource(star_id) {
    star_id = star_id + ""
    text_args = "industy_tag0o_author_id"+star_id+"platform_channel1platform_source1service_methodGetAuthorLinkScoreservice_namedata_space.AdStarDataSpaceServicesign_strict1e39539b8836fb99e1538974d3ac1fe98"
    n = undefined
    result = t.bytesToHex(t.wordsToBytes(a(text_args, n)))
    return result
}
// 传播表现
function getAuthorSpreadInfo(star_id) {
    star_id = star_id + ""
    text_args = "o_author_id"+star_id+"platform_channel1platform_source1range2service_methodGetAuthorSpreadInfoservice_namedata_space.AdStarDataSpaceServicesign_strict1type1e39539b8836fb99e1538974d3ac1fe98"
    n = undefined
    result = t.bytesToHex(t.wordsToBytes(a(text_args, n)))
    return result
}
// 受众画像
function getAuthorWatchedDistribution(star_id) {
    star_id = star_id + ""
    text_args = "o_author_id"+star_id+"platform_channel1platform_source1service_methodGetAuthorWatchedDistributionservice_namedata.AdStarDataServicesign_strict1type1e39539b8836fb99e1538974d3ac1fe98"
    n = undefined
    result = t.bytesToHex(t.wordsToBytes(a(text_args, n)))
    return result
}
star_id = "6952745739747328036"
console.log(getAuthorWatchedDistribution(star_id))