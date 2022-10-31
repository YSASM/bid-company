arguments = ["/api/search/searchmind?mindkeywords=true&mindtype=9&pagesize=5&person=true&searchkey=%e5%8a%b3%e4%bf%9d&suggest=true"]

// 环境变量
o = {
    "default": {
        "n": 20,
        "codes": {
            "0": "W",
            "1": "l",
            "2": "k",
            "3": "B",
            "4": "Q",
            "5": "g",
            "6": "f",
            "7": "i",
            "8": "i",
            "9": "r",
            "10": "v",
            "11": "6",
            "12": "A",
            "13": "K",
            "14": "N",
            "15": "k",
            "16": "4",
            "17": "L",
            "18": "1",
            "19": "8"
        }
    }
}
// key加密函数
function get_en (arguments) {
    for (var e = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase(), t = e + e, n = "", i = 0; i < t.length; ++i) {
        var a = t[i].charCodeAt() % o.default.n;
        n += o.default.codes[a]
    }
    console.log(n.length)
    return n
}
get_en(arguments)