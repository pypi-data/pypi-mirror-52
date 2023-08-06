# import ziloreapi
import ujson
from api import Api

a = Api('17148b85-d7c5-8228-6236-00006a8fe204')
# b = a.add_mf_address('csie.rocks', 'admin', 'clyang@clyang.net')
# b = a.update_mf_address('csie.rocks', 241, destination='clyang@gmail.com')
# b = a.delete_custom_template(527)
# b = a.add_custom_template_record(template_id=527, record_type='txt', record_value='testtest', record_name='zzz')
b = a.delete_custom_template_record(527, [207,208])
print(ujson.dumps(b))

b = a.list_custom_templates()


# b = a.add_record('csie.io','A',600,'test','10.0.0.0')
# print(b['status'])
# b = a.update_record('csie.rocks', 103293, 'CNAME', 300, 'test', 'sdkjlfsdkfs.sdfsf.net')
#b = a.restore_snapshot('csie.rocks', 1024765)
print(ujson.dumps(b))
