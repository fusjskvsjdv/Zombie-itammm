#━━━━━━━━━━━━━━━━━━━
#𝗠𝗔𝗗𝗘 𝗕𝗬 𝗙𝗢𝗫 x 𝗟7𝗔𝗝
#𝗣𝗥𝗢𝗝𝗘𝗖𝗧𝗦 𝗙𝗢𝗫𝗫
#𝗠𝗬 𝗨𝗦𝗘𝗥 : @illllillilllli
#━━━━━━━━━━━━━━━━━━━
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from flask import Flask, request, jsonify
from typing import List

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
app = Flask(__name__)
app.title = "FreeFire Items API"
app.description = "API لإرسال العناصر إلى FreeFire"

freefire_version = "OB50"
API_BASE_URL = "https://projects-fox-x-get.vercel.app/api"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    30,
    0,
    '',
    'data.proto'
)
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndata.proto\"7\n\x12InnerNestedMessage\x12\x0f\n\x07\x66ield_6\x18\x06 \x01(\x03\x12\x10\n\x08\x66ield_14\x18\x0e \x01(\x03\"\x87\x01\n\nNestedItem\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x0f\n\x07\x66ield_3\x18\x03 \x01(\x05\x12\x0f\n\x07\x66ield_4\x18\x04 \x01(\x05\x12\x0f\n\x07\x66ield_5\x18\x05 \x01(\x05\x12$\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\x13.InnerNestedMessage\"@\n\x0fNestedContainer\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12\x1c\n\x07\x66ield_2\x18\x02 \x03(\x0b\x32\x0b.NestedItem\"A\n\x0bMainMessage\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12!\n\x07\x66ield_2\x18\x02 \x03(\x0b\x32\x10.NestedContainerb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_INNERNESTEDMESSAGE']._serialized_start=14
  _globals['_INNERNESTEDMESSAGE']._serialized_end=69
  _globals['_NESTEDITEM']._serialized_start=72
  _globals['_NESTEDITEM']._serialized_end=207
  _globals['_NESTEDCONTAINER']._serialized_start=209
  _globals['_NESTEDCONTAINER']._serialized_end=273
  _globals['_MAINMESSAGE']._serialized_start=275
  _globals['_MAINMESSAGE']._serialized_end=340

key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

def get_jwt_from_access(access_token: str) -> str:
    """
    يحول access token إلى JWT باستخدام API خارجي
    """
    try:
        url = f"{API_BASE_URL}/{access_token}"
        print(f"🔗 الاتصال بالAPI: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"📡 حالة الاستجابة: {response.status_code}")
        print(f"📦 محتوى الاستجابة: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"📊 بيانات JSON: {data}")
                
                # البحث عن JWT في مختلف الأماكن المحتملة
                jwt_token = None
                
                if isinstance(data, dict):
                    if "jwt" in data:
                        jwt_token = data["jwt"]
                    elif "token" in data:
                        jwt_token = data["token"]
                    elif "access_token" in data:
                        jwt_token = data["access_token"]
                    elif "data" in data and isinstance(data["data"], dict):
                        if "jwt" in data["data"]:
                            jwt_token = data["data"]["jwt"]
                
                if jwt_token:
                    print(f"✅ تم الحصول على JWT: {jwt_token[:50]}...")
                    return jwt_token
                else:
                    print("❌ لم يتم العثور على JWT في الاستجابة")
                    return None
                    
            except json.JSONDecodeError:
                # إذا كانت الاستجابة نصاً عادياً وليست JSON
                response_text = response.text.strip()
                print(f"📝 استجابة نصية: {response_text[:100]}...")
                
                # التحقق إذا كانت الاستجابة هي JWT مباشرة
                if response_text.count('.') == 2 and len(response_text) > 100:
                    print("✅ تم الحصول على JWT مباشرة من الاستجابة")
                    return response_text
                else:
                    print("❌ الاستجابة ليست JSON ولا JWT صالح")
                    return None
        else:
            print(f"❌ فشل في الحصول على JWT: {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في الاتصال بالAPI: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {str(e)}")
        return None

@app.route("/get", methods=["GET"])
def send_items():
    """
    إرسال عناصر إلى حساب FreeFire باستخدام access token وقائمة من العناصر.
    """
    
    access = request.args.get('access')
    itemid = request.args.getlist('itemid', type=int)
    
    if not access:
        return jsonify({"status": "error", "message": "يجب إدخال access token"}), 400
    
    if len(itemid) != 15:
        return jsonify({"status": "error", "message": "يجب إدخال 15 عنصر بالضبط"}), 400
    
    print(f"🔑 Access token المستخدم: {access}")
    print(f"🎯 العناصر المدخلة: {itemid}")
    
    # تحويل access إلى JWT
    jwt_token = get_jwt_from_access(access)
    
    if not jwt_token:
        return jsonify({
            "status": "error", 
            "message": "فشل في الحصول على JWT من API الخارجي",
            "api_url": f"{API_BASE_URL}/{access}"
        }), 400
    
    # تعيين العناصر من القائمة المدخلة
    item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13, item14, item15 = itemid

    data = MainMessage()
    data.field_1 = 1
    container1 = data.field_2.add()
    container1.field_1 = 1
    
    items = [
        {"field_1": 2, "field_4": 1, "field_6": {"field_6": item1}},
        {"field_1": 2, "field_4": 1, "field_5": 4, "field_6": {"field_6": item2}},
        {"field_1": 2, "field_4": 1, "field_5": 2, "field_6": {"field_6": item3}},
        {"field_1": 13, "field_3": 1, "field_6": {"field_6": item4}},
        {"field_1": 13, "field_3": 1, "field_4": 2, "field_6": {"field_6": item5}},
        {"field_1": 13, "field_3": 1, "field_5": 2, "field_6": {"field_6": item6}},
        {"field_1": 13, "field_3": 1, "field_5": 4, "field_6": {"field_6": item7}},
        {"field_1": 13, "field_3": 1, "field_4": 2, "field_5": 2, "field_6": {"field_6": item8}},
        {"field_1": 13, "field_3": 1, "field_4": 2, "field_5": 4, "field_6": {"field_6": item9}},
        {"field_1": 13, "field_3": 1, "field_4": 4, "field_6": {"field_6": item10}},
        {"field_1": 13, "field_3": 1, "field_4": 4, "field_5": 2, "field_6": {"field_6": item11}},
        {"field_1": 13, "field_3": 1, "field_4": 4, "field_5": 4, "field_6": {"field_6": item12}},
        {"field_1": 13, "field_3": 1, "field_4": 6, "field_6": {"field_6": item13}},
        {"field_1": 13, "field_3": 1, "field_4": 6, "field_5": 2, "field_6": {"field_6": item14}},
        {"field_1": 13, "field_3": 1, "field_4": 6, "field_5": 4, "field_6": {"field_6": item15}}
    ]
    
    for item_data in items:
        item = container1.field_2.add()
        item.field_1 = item_data["field_1"]
        if "field_3" in item_data:
            item.field_3 = item_data["field_3"]
        if "field_4" in item_data:
            item.field_4 = item_data["field_4"]
        if "field_5" in item_data:
            item.field_5 = item_data["field_5"]
        item.field_6.field_6 = item_data["field_6"]["field_6"]
    
    container2 = data.field_2.add()
    container2.field_1 = 9
    item7 = container2.field_2.add()
    item7.field_4 = 3
    item7.field_6.field_14 = 3048205855
    item8 = container2.field_2.add()
    item8.field_4 = 3
    item8.field_5 = 3
    item8.field_6.field_14 = 3048205855
    
    data_bytes = data.SerializeToString()
    padded_data = pad(data_bytes, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_data)
    
    url = "https://clientbp.ggblueshark.com/SetPlayerGalleryShowInfo"
    headers = {
        "Expect": "100-continue",
        "Authorization": f"Bearer {jwt_token}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": freefire_version,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
        "Host": "clientbp.ggblueshark.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    
    try:
        print("🚀 إرسال البيانات إلى FreeFire...")
        response = requests.post(url, headers=headers, data=encrypted_data, timeout=30)
        
        print(f"📡 استجابة FreeFire: {response.status_code}")
        print(f"📦 محتوى الاستجابة: {response.text[:200]}...")
        
        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "message": "تم إرسال العناصر بنجاح",
                "status_code": response.status_code,
                "response": response.text
            })
        else:
            return jsonify({
                "status": "error",
                "message": "فشل في إرسال العناصر",
                "status_code": response.status_code,
                "response": response.text
            })
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {str(e)}")
        return jsonify({"status": "error", "message": f"خطأ في الاتصال: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "مرحباً بك في FreeFire Items API", 
        "usage": "استخدم /get?access=YOUR_ACCESS&itemid=ID1&itemid=ID2...",
        "api_endpoint": API_BASE_URL,
        "example": "http://127.0.0.1:8000/get?access=your_token&itemid=90200028&itemid=90200029&itemid=90200030&itemid=90200031&itemid=90200032&itemid=90200033&itemid=90200034&itemid=90200035&itemid=90200036&itemid=90200037&itemid=90200038&itemid=90200039&itemid=90200040&itemid=90200041&itemid=90200042"
    })

@app.route("/debug/<access>", methods=["GET"])
def debug_api(access):
    """لتصحيح استجابة API الخارجي"""
    result = get_jwt_from_access(access)
    if result:
        return jsonify({"status": "success", "jwt": result[:100] + "..."})
    else:
        return jsonify({"status": "error", "message": "فشل في الحصول على JWT"})

if __name__ == "__main__":
    print("🚀 تشغيل FreeFire Items API...")
    print(f"🌐 العنوان: http://127.0.0.1:8000")
    print(f"🔗 API المستهدف: {API_BASE_URL}")
    app.run(host="0.0.0.0", port=8000, debug=True)