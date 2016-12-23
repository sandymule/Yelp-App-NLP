import logging
import json
import Levenshtein
import numpy as np

from flask import render_template
from flask_wtf import Form
from wtforms import fields
from wtforms.validators import Required

from . import app, highlights, business, mat_index#, review_vec


logger = logging.getLogger('app')

class PredictForm(Form):

    biz_name_input = fields.TextField('Business Name: ', validators=[Required()])
    submit = fields.SubmitField('Submit')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = PredictForm()
    highlights_list = None
    restaurants = None
    test_vec = None

    if form.validate_on_submit():
        # store the submitted values
        submitted_data = form.data

        biz_name_input = str(submitted_data['biz_name_input'])
        biz_id = nametoindex(biz_name_input)
        #highlights_list = highlights.ix[biz_id, 1].split()

        idx = highlights[highlights[0] == biz_id].index.tolist()
        highlights_list = highlights.ix[idx[0],1].split()

        test_vec = [(0, 0.09148784),
 (1, 0.1140965),
 (2, 0.15647799),
 (3, 0.064791605),
 (4, 0.044292003),
 (5, -0.21004641),
 (6, -0.21589896),
 (7, -0.086651228),
 (8, -0.13115928),
 (9, 0.063104704),
 (10, -0.15348472),
 (11, 0.002090025),
 (12, -0.037396401),
 (13, 0.59416705),
 (14, -0.16895559),
 (15, -0.1263859),
 (16, -0.050156903),
 (17, 0.25533599),
 (18, -0.12874311),
 (19, 0.46221739),
 (20, -0.29962602),
 (21, 0.025056994),
 (22, -0.14912479),
 (23, -0.1381364),
 (24, 0.022632098),
 (25, -0.355701),
 (26, -0.179893),
 (27, 0.022246799),
 (28, -0.12758121),
 (29, -0.44335452),
 (30, -0.53142941),
 (31, 0.16145352),
 (32, -0.1531394),
 (33, -0.20848601),
 (34, -0.21042421),
 (35, 0.39753279),
 (36, 0.11235468),
 (37, -0.091336496),
 (38, -0.2630116),
 (39, -0.026586318),
 (40, 0.289345),
 (41, -0.30375224),
 (42, 0.23273261),
 (43, -0.057532776),
 (44, 0.050063897),
 (45, 0.069545403),
 (46, 0.32142273),
 (47, 0.2919172),
 (48, -0.38489699),
 (49, 0.099316999),
 (50, -0.28416389),
 (51, -0.18418109),
 (52, 0.1821095),
 (53, 0.2076201),
 (54, -0.17680711),
 (55, -0.23066001),
 (56, -0.14282361),
 (57, 0.081737004),
 (58, 0.13534445),
 (59, 0.014678407),
 (60, 0.3231582),
 (61, -0.40911904),
 (62, -0.11453829),
 (63, 0.021452151),
 (64, -0.1032048),
 (65, 0.036625206),
 (66, -0.20529127),
 (67, 0.15244161),
 (68, -0.062042315),
 (69, -0.29554719),
 (70, 0.18731821),
 (71, 0.097501591),
 (72, -0.010075006),
 (73, -0.15883221),
 (74, -0.25673971),
 (75, 0.090723649),
 (76, 0.45151934),
 (77, 0.27888003),
 (78, -0.31888929),
 (79, 0.065122105),
 (80, -0.21737643),
 (81, 0.14750791),
 (82, -0.15219572),
 (83, 0.094605103),
 (84, 0.1943773),
 (85, -0.011671555),
 (86, -0.23487639),
 (87, 0.0804203),
 (88, -0.26992059),
 (89, -0.16141252),
 (90, 0.46480003),
 (91, 0.072837293),
 (92, 0.2025346),
 (93, -0.053851493),
 (94, -0.13599232),
 (95, 0.079440497),
 (96, 0.0519333),
 (97, 0.38224399),
 (98, -0.20978031),
 (99, 0.27874568),
 (100, 0.097790092),
 (101, -0.12553521),
 (102, 0.107758),
 (103, -0.435491),
 (104, -0.66543895),
 (105, -0.17786379),
 (106, 0.070285991),
 (107, 0.0064580142),
 (108, -0.095397703),
 (109, 0.20358777),
 (110, 0.50356138),
 (111, 0.3168672),
 (112, -0.016336199),
 (113, -0.56706041),
 (114, 0.0067259027),
 (115, -0.13349882),
 (116, -0.2989077),
 (117, 0.34156859),
 (118, 0.50306165),
 (119, 0.11159702),
 (120, -0.23304519),
 (121, -0.16753998),
 (122, 0.24013369),
 (123, 0.23769739),
 (124, -0.14970759),
 (125, 0.010008201),
 (126, -0.16903211),
 (127, 0.0028184026),
 (128, -0.094317593),
 (129, 0.37782496),
 (130, 0.178892),
 (131, 0.34438151),
 (132, 0.03971016),
 (133, 0.24611051),
 (134, 0.016337298),
 (135, -0.0962127),
 (136, 0.043509595),
 (137, 0.070600905),
 (138, -0.144729),
 (139, 0.022237608),
 (140, 0.31699303),
 (141, 0.1904349),
 (142, -0.2243031),
 (143, -0.034984618),
 (144, -0.13349257),
 (145, 0.13367939),
 (146, -0.077951454),
 (147, -0.29093498),
 (148, 0.23460801),
 (149, -0.25573373),
 (150, -0.65452397),
 (151, 0.31135002),
 (152, 0.189311),
 (153, 0.071926899),
 (154, -0.3307189),
 (155, -0.24479702),
 (156, -0.026526298),
 (157, -0.00076218246),
 (158, -0.13405672),
 (159, -0.13419798),
 (160, 0.051778954),
 (161, -0.023234),
 (162, -0.13616419),
 (163, -0.038656805),
 (164, 0.19009309),
 (165, -0.018110137),
 (166, 0.110954),
 (167, -0.1935996),
 (168, 0.14189979),
 (169, -0.42203632),
 (170, -0.036326095),
 (171, -0.10470231),
 (172, 0.021857996),
 (173, 0.090515204),
 (174, -0.20213142),
 (175, -0.11904861),
 (176, 0.022493901),
 (177, -0.065964699),
 (178, 0.4546946),
 (179, -0.37633759),
 (180, 0.0702518),
 (181, 0.082814112),
 (182, 0.098101698),
 (183, -0.18618701),
 (184, 0.095640406),
 (185, 0.026103279),
 (186, 0.17188901),
 (187, 0.21274927),
 (188, 0.14722738),
 (189, 0.039358556),
 (190, 0.019174702),
 (191, 0.65125972),
 (192, -0.15365036),
 (193, 0.11124711),
 (194, 0.30078098),
 (195, -0.1225544),
 (196, -0.20826352),
 (197, -0.1171219),
 (198, -0.1467429),
 (199, 0.073925689),
 (200, 0.013208091),
 (201, -0.17910449),
 (202, 0.46272787),
 (203, 0.37973469),
 (204, 0.016960591),
 (205, 0.1137659),
 (206, 0.046910692),
 (207, 0.040940009),
 (208, 0.109759),
 (209, -0.1269747),
 (210, 0.289419),
 (211, -0.14326121),
 (212, -0.1398015),
 (213, 0.12836429),
 (214, 0.069987103),
 (215, -0.013861599),
 (216, 0.50625902),
 (217, -0.46981168),
 (218, -0.095453903),
 (219, 0.030295003),
 (220, 0.14663498),
 (221, 0.088777885),
 (222, -0.33487269),
 (223, -0.1711829),
 (224, -0.3841607),
 (225, -0.52149802),
 (226, -0.028016701),
 (227, -0.15551399),
 (228, -0.1125109),
 (229, 0.079002127),
 (230, 0.22019832),
 (231, 0.12998089),
 (232, -0.19011641),
 (233, -0.086826906),
 (234, 0.59640104),
 (235, 0.075161099),
 (236, 0.15514569),
 (237, 0.22172502),
 (238, -0.33589423),
 (239, -0.040563207),
 (240, -0.1549633),
 (241, -0.28516766),
 (242, -0.14296159),
 (243, -0.013414474),
 (244, -0.16514072),
 (245, 0.21770294),
 (246, 0.047903195),
 (247, 0.041246805),
 (248, -0.2295502),
 (249, -0.63969928),
 (250, 0.35804862),
 (251, 0.12614019),
 (252, 0.084889099),
 (253, 0.14469442),
 (254, 0.15521027),
 (255, 0.22462079),
 (256, -0.032963205),
 (257, 0.074373208),
 (258, -0.041092098),
 (259, 0.13307719),
 (260, 0.1325949),
 (261, -0.30755022),
 (262, 0.19033769),
 (263, -0.024342697),
 (264, 0.057743013),
 (265, -0.24844071),
 (266, -0.12020596),
 (267, 0.2454627),
 (268, 0.075425006),
 (269, -0.17668898),
 (270, -0.097151801),
 (271, 0.020849098),
 (272, -0.22346351),
 (273, 0.38478673),
 (274, -0.047789987),
 (275, 0.15994692),
 (276, -0.38727),
 (277, -0.31316665),
 (278, -0.68865699),
 (279, -0.19504289),
 (280, -0.057241596),
 (281, 0.17456952),
 (282, -0.017044071),
 (283, 0.2233675),
 (284, 0.21197005),
 (285, 0.10130219),
 (286, 0.28425971),
 (287, -0.039406698),
 (288, 0.25872129),
 (289, -0.032786779),
 (290, 0.040430121),
 (291, 0.095782101),
 (292, 0.14410801),
 (293, -0.087634161),
 (294, -0.38744301),
 (295, -0.36683768),
 (296, 0.024050456),
 (297, -0.38267711),
 (298, 0.26452389),
 (299, 0.031707801)]
        
        
        restaurants = get_restaurants(biz_id, test_vec)

    return render_template('index.html',
        form=form,
        highlights_list=highlights_list,
        restaurants=restaurants)

def nametoindex(myname):
    distances = []
    for i in range(len(business)):
        biz_name = business.iloc[i,:][9]
        new_word = []
        for word in biz_name.split():
            new_word.append(''.join([l for l in word if l.isalpha()]))
        biz_new_name = ' '.join(new_word)
        distances.append(Levenshtein.distance(myname, str(biz_new_name.encode('utf-8'))))

    biz_index = distances.index(min(distances))
    return business['business_id'][biz_index]

def get_restaurants(biz_id, test_vec):
    #row = highlights.index.get_loc(biz_id)
    sims = sorted(enumerate(mat_index[test_vec]), key=lambda item: -item[1])
    indexes = [i[0] for i in sims[:30]]
    biz_ids = highlights[0][indexes].tolist()
    return business[business.business_id.isin(biz_ids)].name.tolist()


