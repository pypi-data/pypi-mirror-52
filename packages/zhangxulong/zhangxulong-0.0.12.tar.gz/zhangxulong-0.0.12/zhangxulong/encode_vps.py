import base64
# from qrtools.qrtools import QR
# import pyqrcode


# def qrcode_gen_dec(qrcode_path, qrcode_data=None):
#     '''
#
#     :param qrcode_path: read or save qr.png
#     :param qrcode_data: save data  to  qr
#     :return:
#     '''
#     if qrcode_data is None:
#         qr = QR()
#         qr.decode(qrcode_path)
#
#         return qr.data
#     else:
#         qr = pyqrcode.create(qrcode_data)
#         qr.png(qrcode_path, scale=6)
#
#         return qrcode_path


def encode_ssr_file_to_b64(tobe_encode_file, output_file):
    with open(tobe_encode_file, 'rb') as fin:
        ba_en = base64.b64encode(fin.read())
        with open(output_file, 'wb') as ba_en_f:
            ba_en_f.write(ba_en)
    return 0


def encode_data_to_b64(tobe_encode, output_file):
    ba_en = base64.b64encode(tobe_encode.encode())
    with open(output_file, 'wb') as ba_en_f:
        ba_en_f.write(ba_en)
    return 0


if __name__ == '__main__':
    str_list = [
        'vmess://bm9uZTpjM2VhYTY1OS0xMDdkLTQ4OWEtYTYyYy0zZmUxMjBkOTk2ZmRAY2hpLnpoYW5neHVsb25nLnh5ejo0NDM?remarks=vultr&obfsParam=chi.zhangxulong.xyz&path=/e11201f7/&obfs=websocket&tls=1\nssr://MTYyLjIxOS4xMjMuMTc3Ojg4OmF1dGhfc2hhMV92NDphZXMtMjU2LWNmYjpwbGFpbjpNQS8_cmVtYXJrcz1jWEV0Y2cmcHJvdG9wYXJhbT0mb2Jmc3BhcmFtPQ\nvmess://YWVzLTEyOC1jZmI6MDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwQDE2Mi4yMTkuMTIzLjE3NzoxMDA4Ng?remarks=qq-v\nssr://NjUuNDkuMjA0LjIzNjo4ODphdXRoX3NoYTFfdjQ6YWVzLTI1Ni1jZmI6cGxhaW46TUEvP3JlbWFya3M9WW14aFkyc3RjZyZwcm90b3BhcmFtPSZvYmZzcGFyYW09\nvmess://bm9uZTowMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDBANjUuNDkuMjA0LjIzNjoxMDA4Ng?remarks=black-v\nssr://NDUuMTEuMC4zODo4MDphdXRoX3NoYTFfdjQ6YWVzLTI1Ni1jZmI6aHR0cF9zaW1wbGU6YzJGa1ptRnpaQS8_cmVtYXJrcz1jMmhoY21VJnByb3RvcGFyYW09Jm9iZnNwYXJhbT0\nvmess://bm9uZTpmMTYxZjlmYy1jZjc3LTRlYWUtOGMwMS04MGY3YTQ0MWFkMWFAdnBzLnpoYW5neHVsb25nLnh5ejo0NDM?remarks=gmail&obfsParam=vps.zhangxulong.xyz&path=/9cf1e718/&obfs=websocket&tls=1',

        ]
    num = 0
    for item in str_list:
        num += 1
        encode_data_to_b64(item, '../encode%d' % num)

    # encode_data_to_b64('vmess://bm9uZTpmMTYxZjlmYy1jZjc3LTRlYWUtOGMwMS04MGY3YTQ0MWFkMWFAdnBzLnpoYW5neHVsb25nLnh5ejo0NDM?remarks=200%20%E5%85%B1%E4%BA%AB%E7%89%88vps&obfsParam=vps.zhangxulong.xyz&path=/9cf1e718/&obfs=websocket&tls=1','../encode')
    # encode_data_to_b64(qrcode_gen_dec('../qr.png'),'../encode')
    # encode_ssr_file_to_b64('../ssr.txt', '../ssr.encode')
