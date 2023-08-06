import {ModalPopup} from "../../utils/js/modal_popup.js"
import {FieldValidator, EnableValidation} from "../../utils/js/form_validation.js"


window.addEventListener('load', function () {

    // MODAL POPUPS
    const email_modal_popup = new ModalPopup(`<h2>Adresse email</h2>
                                             <p>Pour être valide, l'adresse email doit :</p>
                                             <ul>
                                                 <li>avoir un format du type "username@domaine.extension".</li>
                                                 <li>avoir une longueur minimale de 6 caractères et une longueur maximale de 255 caractères.</li>
                                             </ul>
                                             <br/>
                                             <br/>
                                             <p>Pour être valide, la partie "username" de l'adresse doit :</p>
                                             <ul>
                                                 <li>avoir une longueur minimale de 1 caractère et une longeur maximale de 250 caractères.</li>
                                                 <li>commencer par une lettre, un chiffre, "-", "_" ou "%".</li>
                                                 <li>contenir uniquement des lettres, des chiffres, "-", "_", "%", "+" ou des ".".</li>
                                             </ul>
                                             <p>Pour être valide, la partie "username" ne doit pas :</p>
                                             <ul>
                                                 <li>contenir de doubles "-" ni de doubles ".".</li>  
                                                 <li>se terminer par "+", "." ou "-".</li> 
                                             </ul>
                                             <br/>
                                             <br/>
                                             <p>Pour être valide, la partie "domain" doit :</p>
                                             <ul>
                                                 <li>avoir une longueur minimale de 1 caractère et une longeur maximale de 250 caractères.</li>
                                                 <li>commencer par une lettre, un chiffre, "-", "_" ou "%".</li>
                                                 <li>contenir uniquement des lettres, des chiffres, "-", "_", "%", ou des "+".</li>
                                             </ul>
                                             <p>Pour être valide, la partie "domain" ne doit pas :</p>
                                             <ul>
                                                 <li>contenir de doubles "-".</li>  
                                                 <li>se terminer par "+", ou "-".</li> 
                                             </ul>
                                             <br/>
                                             <br/>
                                             <p>Pour être valide, la partie "extension" doit :</p>
                                             <ul>
                                                 <li>avoir une longueur minimale de 2 caractères.</li>
                                                 <li>être composée de lettres minuscules uniquement.</li>
                                             </ul>
                                             `);

    const password_modal_popup = new ModalPopup(`<h2>Mot de passe</h2>
                                                <p>Le mot de passe peut contenir n'importe quel caractère existant.</p>
                                                <br/>
                                                <p>Pour être valide, le mot de passe doit :</p>
                                                <ul>
                                                    <li>avoir une longueur minimale de 10 caractères et une longueur maximale de 255 caractères.</li>
                                                    <li>contenir au moins un chiffre.</li>
                                                    <li>contenir au moins un caractère spécial. Vous pouvez utiliser notre <a href="#" class="special-characters-list-button">outil pour les caractères spéciaux</a> qui permet de voir et copier facilement un caractère spécial parmis tous ceux existants. </li>
                                                </ul>
                                                `);

    // FIELDS VALIDATION.
    const email_validation = new FieldValidator("admin_login_form",
                                                "email",
                                                "adresse email",
                                                "une",
                                                "cette",
                                                true,
                                                null,
                                                255,
                                                "^([a-zA-Z0-9_%+](\\.|\\-)?){0,249}[a-zA-Z0-9_%]@([a-zA-Z0-9_%+]\\-?){0,249}[a-zA-Z0-9_%]\\.[a-z]{2,}$",
                                                null,
                                                false,
                                                true,
                                                "exists",
                                                email_modal_popup);

    const password_validation = new FieldValidator("admin_login_form",
                                                   "password",
                                                   "mot de passe",
                                                   "un",
                                                   "ce",
                                                   true,
                                                   10,
                                                   255,
                                                   "^((.*)?[૱┯┰┱┲❗►◄ĂăǕǖꞀ¤Ð¢℥Ω℧Kℶℷℸⅇ⅊⚌⚍⚎⚏⚭⚮⌀⏑⏒⏓⏔⏕⏖⏗⏘⏙⏠⏡⏦ᶀᶁᶂᶃᶄᶆᶇᶈᶉᶊᶋᶌᶍᶎᶏᶐᶑᶒᶓᶔᶕᶖᶗᶘᶙᶚᶸᵯᵰᵴᵶᵹᵼᵽᵾᵿ  ‎‏ ⁁⁊ ⁪⁫⁬⁭⁮⁯⸜⸝¶¥£⅕⅙⅛⅔⅖⅗⅘⅜⅚⅐⅝↉⅓⅑⅒⅞←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯↰↱↲↳↴↵↶↷↸↹↺↻↼↽↾↿⇀⇁⇂⇃⇄⇅⇆⇇⇈⇉⇊⇋⇌⇍⇎⇏⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙⇚⇛⇜⇝⇞⇟⇠⇡⇢⇣⇤⇥⇦⇨⇩⇪⇧⇫⇬⇭⇮⇯⇰⇱⇲⇳⇴⇵⇶⇷⇸⇹⇺⇻⇼⇽⇾⇿⟰⟱⟲⟳⟴⟵⟶⟷⟸⟹⟺⟻⟼⟽⟾⟿⤀⤁⤂⤃⤄⤅⤆⤇⤈⤉⤊⤋⤌⤍⤎⤏⤐⤑⤒⤓⤔⤕⤖⤗⤘⤙⤚⤛⤜⤝⤞⤟⤠⤡⤢⤣⤤⤥⤦⤧⤨⤩⤪⤫⤬⤭⤮⤯⤰⤱⤲⤳⤴⤵⤶⤷⤸⤹⤺⤻⤼⤽⤾⤿⥀⥁⥂⥃⥄⥅⥆⥇⥈⥉⥊⥋⥌⥍⥎⥏⥐⥑⥒⥓⥔⥕⥖⥗⥘⥙⥚⥛⥜⥝⥞⥟⥠⥡⥢⥣⥤⥥⥦⥧⥨⥩⥪⥫⥬⥭⥮⥯⥰⥱⥲⥳⥴⥵⥶⥷⥸⥹⥺⥻⥼⥽⥾⥿➔➘➙➚➛➜➝➞➝➞➟➠➡➢➣➤➥➦➧➨➩➩➪➫➬➭➮➯➱➲➳➴➵➶➷➸➹➺➻➼➽➾⬀⬁⬂⬃⬄⬅⬆⬇⬈⬉⬊⬋⬌⬍⬎⬏⬐⬑☇☈⏎⍃⍄⍅⍆⍇⍈⍐⍗⍌⍓⍍⍔⍏⍖♾⎌☊☋☌☍⌃⌄⌤⌅⌆⌇⚋⚊⌌⌍⌎⌏⌐⌑⌔⌕⌗⌙⌢⌣⌯⌬⌭⌮⌖⌰⌱⌲⌳⌴⌵⌶⌷⌸⌹⌺⌻⌼⍯⍰⌽⌾⌿⍀⍁⍂⍉⍊⍋⍎⍏⍑⍒⍕⍖⍘⍙⍚⍛⍜⍝⍞⍠⍟⍡⍢⍣⍤⍥⍨⍩⍦⍧⍬⍿⍪⍮⍫⍱⍲⍭⍳⍴⍵⍶⍷⍸⍹⍺⍼⍽⍾⎀⎁⎂⎃⎄⎅⎆⎉⎊⎋⎍⎎⎏⎐⎑⎒⎓⎔⎕⏣⌓⏥⏢⎖⎲⎳⎴⎵⎶⎸⎹⎺⎻⎼⎽⎾⎿⏀⏁⏂⏃⏄⏅⏆⏇⏈⏉⏉⏋⏌⏍⏐⏤⏚⏛Ⓝℰⓦ!   ⌘«»‹›‘’“”„‚❝❞£¥€$¢¬¶@§®©™°×π±√‰Ω∞≈÷~≠¹²³½¼¾‐–—|⁄\\[\\]{}†‡…·•●⌥⌃⇧↩¡¿‽⁂∴∵◊※←→↑↓☜☞☝☟✔★☆♺☼☂☺☹☃✉✿✄✈✌✎♠♦♣♥♪♫♯♀♂αßÁáÀàÅåÄäÆæÇçÉéÈèÊêÍíÌìÎîÑñÓóÒòÔôÖöØøÚúÙùÜüŽž₳฿￠€₡¢₢₵₫￡£₤₣ƒ₲₭₥₦₱＄$₮₩￦¥￥₴₰¤៛₪₯₠₧₨௹﷼㍐৲৳~ƻƼƽ¹¸¬¨ɂǁ¯Ɂǂ¡´°ꟾ¦}{|\\.,·\\]\\)\\[/_\\¿º§\\\"\\*\\-\\+\\(!&%$¼¾½¶©®@ẟⱿ`Ȿ^꜠꜡ỻ'=:<;ꞌꞋ꞊ꞁ꞉>?÷ℾℿ℔℩℉⅀℈þðÞµªꝋꜿꜾⱽⱺⱹⱷⱶⱵⱴⱱⱰⱦȶȴȣȢȡȝȜțȋȊȉȈǯǮǃǀƿƾƺƹƸƷƲưƪƣƢƟƛƖƕƍſỽ⸀⸁⸂⸃⸄⸅⸆⸇⸈⸉⸊⸋⸌⸍⸎⸏⸐⸑⸒⸔⸕▲▼◀▶◢◣◥◤△▽◿◺◹◸▴▾◂▸▵▿◃▹◁▷◅▻◬⟁⧋⧊⊿∆∇◭◮⧩⧨⌔⟐◇◆◈⬖⬗⬘⬙⬠⬡⎔⋄◊⧫⬢⬣▰▪◼▮◾▗▖■∎▃▄▅▆▇█▌▐▍▎▉▊▋❘❙❚▀▘▝▙▚▛▜▟▞░▒▓▂▁▬▔▫▯▭▱◽□◻▢⊞⊡⊟⊠▣▤▥▦⬚▧▨▩⬓◧⬒◨◩◪⬔⬕❏❐❑❒⧈◰◱◳◲◫⧇⧅⧄⍁⍂⟡⧉○◌◍◎◯❍◉⦾⊙⦿⊜⊖⊘⊚⊛⊝●⚫⦁◐◑◒◓◔◕⦶⦸◵◴◶◷⊕⊗⦇⦈⦉⦊❨❩⸨⸩◖◗❪❫❮❯❬❭❰❱⊏⊐⊑⊒◘◙◚◛◜◝◞◟◠◡⋒⋓⋐⋑╰╮╭╯⌒╳✕╱╲⧸⧹⌓◦❖✖✚✜⧓⧗⧑⧒⧖_⚊╴╼╾‐⁃ ‒\\-–⎯—―╶╺╸─━┄┅┈┉╌╍═≣≡☰☱☲☳☴☵☶☷╵╷╹╻│▕▏┃┆┇┊╎┋╿╽┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╏║╔╒╓╕╖╗╚╘╙╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬⌞⌟⌜⌝⌊⌋⌉⌈⌋₯ἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏἐἑἒἓἔἕἘἙἚἛἜἝἠἡἢἣἤἥἦἧἨἩἪἫἬἭἮἯἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὀὁὂὃὄὅὈὉὊὋὌὍὐὑὒὓὔὕὖὗὙὛὝὟὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὰάὲέὴήὶίὸόὺύὼώᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼ᾽ι᾿῀῁ῂῃῄῆῇῈΈῊΉῌ῍῎῏ῐῑῒΐῖῗῘῙῚΊ῝῞῟ῠῡῢΰῤῥῦῧῨῩῪΎῬ῭΅`ῲῳῴῶῷῸΌῺΏῼ´῾ͰͱͲͳʹ͵Ͷͷͺͻͼͽ;΄΅Ά·ΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΪΫάέήίΰαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώϐϑϒϓϔϕϖϗϘϙϚϛϜϝϞϟϠϡϢϣϤϥϦϧϨϩϪϫϬϭϮϯϰϱϲϳϴϵ϶ϷϸϹϺϻϼϽϾϿⒶⓐ⒜ẠạẢảḀḁÂÃǍǎẤấẦầẨẩȂȃẪẫẬậÀÁẮắẰằẲẳẴẵẶặĀāĄąǞȀȁÅǺǻÄäǟǠǡâáåãàẚȦȧȺÅⱥÆæǼǢǣⱯꜲꜳꜸꜺⱭꜹꜻª℀⅍℁Ⓑⓑ⒝ḂḃḄḅḆḇƁɃƀƃƂƄƅℬⒸⓒ⒞ḈḉĆćĈĉĊċČčÇçƇƈȻȼℂ℃ℭƆ℅℆℄ꜾꜿⒹⓓ⒟ḊḋḌḍḎḏḐḑḒḓĎďƊƋƌƉĐđȡⅅⅆǱǲǳǄǅǆȸⒺⓔ⒠ḔḕḖḗḘḙḚḛḜḝẸẹẺẻẾếẼẽỀềỂểỄễỆệĒēĔĕĖėĘęĚěÈèÉéÊêËëȄȅȨȩȆȇƎⱸɆℇℯ℮ƐℰƏǝⱻɇⒻⓕ⒡ḞḟƑƒꜰℲⅎꟻℱ℻Ⓖⓖ⒢ƓḠḡĜĝĞğĠġĢģǤǥǦǧǴℊ⅁ǵⒽⓗ⒣ḢḣḤḥḦḧḨḩḪḫẖĤĥȞȟĦħⱧⱨꜦℍǶℏℎℋℌꜧⒾⓘ⒤ḬḭḮḯĲĳìíîïÌÍÎÏĨĩĪīĬĭĮįıƗƚỺǏǐⅈⅉℹℑℐⒿⓙ⒥ĴĵȷⱼɈɉǰⓀⓚ⒦ḰḱḲḳḴḵĶķƘƙꝀꝁꝂꝃꝄꝅǨǩⱩⱪĸⓁⓛ⒧ḶḷḸḹḺḻḼḽĹĺĻļĽİľĿŀŁłỈỉỊịȽⱠꝈꝉⱡⱢꞁℒǇǈǉ⅃⅂ℓȉȈȊȋⓂⓜ⒨ḾḿṀṁṂṃꟿꟽⱮƩƜℳⓃⓝ⒩ṄṅṆṇṈṉṊṋŃńŅņŇňǸǹŊƝñŉÑȠƞŋǊǋǌȵℕ№ṌṍṎṏṐṑṒṓȪȫȬȭȮȯȰȱǪǫǬǭỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợƠơŌōŎŏŐőÒÓÔÕÖǑȌȍȎȏŒœØǾꝊǽǿℴ⍥⍤Ⓞⓞ⒪òóôõöǒøꝎꝏⓅⓟ⒫℗ṔṕṖṗƤƥⱣℙǷꟼ℘Ⓠⓠ⒬Ɋɋℚ℺ȹⓇⓡ⒭ŔŕŖŗŘřṘṙṚṛṜṝṞṟȐȑȒȓɍɌƦⱤ℞Ꝛꝛℜℛ℟ℝⓈⓢ⒮ṠṡṢṣṤṥṦṧṨṩŚśŜŝŞşŠšȘșȿꜱƧƨẞßẛẜẝ℠Ⓣⓣ⒯ṪṫṬṭṮṯṰṱŢţŤťŦŧƬƮẗȚȾƫƭțⱦȶ℡™Ⓤⓤ⒰ṲṳṴṵṶṷṸṹṺṻỤỦủỨỪụứỬửừữỮỰựŨũŪūŬŭŮůŰűǙǚǗǘǛǜŲųǓǔȔȕÛûȖȗÙùÜüƯúɄưƲƱⓋⓥ⒱ṼṽṾṿỼɅ℣ⱱⱴⱽⓌⓦ⒲ẀẁẂẃẄẅẆẇẈẉŴŵẘⱲⱳⓍⓧ⒳ẊẋẌẍℵ×Ⓨⓨ⒴ẎẏỾỿẙỲỳỴỵỶỷỸỹŶŷƳƴŸÿÝýɎɏȲƔ⅄ȳℽⓏⓩ⒵ẐẑẒẓẔẕŹźŻżŽžȤȥⱫⱬƵƶɀℨℤ⟀⟁⟂⟃⟄⟇⟈⟉⟊⟐⟑⟒⟓⟔⟕⟖⟗⟘⟙⟚⟛⟜⟝⟞⟟⟠⟡⟢⟣⟤⟥⟦⟧⟨⟩⟪⟫⦀⦁⦂⦃⦄⦅⦆⦇⦈⦉⦊⦋⦌⦍⦎⦏⦐⦑⦒⦓⦔⦕⦖⦗⦘⦙⦚⦛⦜⦝⦞⦟⦠⦡⦢⦣⦤⦥⦦⦧⦨⦩⦪⦫⦬⦭⦮⦯⦰⦱⦲⦳⦴⦵⦶⦷⦸⦹⦺⦻⦼⦽⦾⦿⧀⧁⧂⧃⧄⧅⧆⧇⧈⧉⧊⧋⧌⧍⧎⧏⧐⧑⧒⧓⧔⧕⧖⧗⧘⧙⧚⧛⧜⧝⧞⧟⧡⧢⧣⧤⧥⧦⧧⧨⧩⧪⧫⧬⧭⧮⧯⧰⧱⧲⧳⧴⧵⧶⧷⧸⧹⧺⧻⧼⧽⧾⧿∀∁∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿≀≁≂≃≄≅≆≇≈≉≊≋≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≤≥≦≧≨≩≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿✕✖✚◀▶❝❞★☆☼☂☺☹✄✈✌✎♪♫☀☁☔⚡❆☽☾✆✔☯☮☠⚑☬✄✏♰✡✰✺⚢⚣♕♛♚♬ⓐⓑⓒⓓ↺↻⇖⇗⇘⇙⟵⟷⟶⤴⤵⤶⤷➫➬€₤＄₩₪⟁⟐◆⎔░▢⊡▩⟡◎◵⊗❖ΩβΦΣΞ⟁⦻⧉⧭⧴∞≌⊕⋍⋰⋱✖⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾ᴕ⸨⸩❪❫⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛⓪①②③④⑤⑥⑦⑧⑨⑩➀➁➂➃➄➅➆➇➈➉⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⓿❶❷❸❹❺❻❼❽❾❿➊➋➌➍➎➏➐➑➒➓⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇ᶅᶛᶜᶝᶞᶟᶠᶡᶢᶣᶤᶥᶦᶧᶨᶩᶪᶫᶬᶭᶮᶯᶰᶱᶲᶳᶴᶵᶶᶷᶹᶺᶻᶼᶽᶾᶿᴀᴁᴂᴃᴄᴅᴆᴇᴈᴉᴊᴋᴌᴍᴎᴏᴐᴑᴒᴓᴔᴕᴖᴗᴘᴙᴚᴛᴜᴝᴞᴟᴠᴡᴢᴣᴤᴥᴦᴧᴨᴩᴪᴫᴬᴭᴮᴯᴰᴱᴲᴳᴴᴵᴶᴷᴸᴹᴺᴻᴼᴽᴾᴿᵀᵁᵂᵃᵄᵅᵆᵇᵈᵉᵊᵋᵌᵍᵎᵏᵐᵑᵒᵓᵔᵕᵖᵗᵘᵙᵚᵛᵜᵝᵞᵟᵠᵡᵢᵣᵤᵥᵦᵧᵨᵩᵪᵫᵬᵭᵮᵱᵲᵳᵵᵷᵸᵺᵻ ᷋ ᷌ ᷍ ᷎ ᷏ ᷓ ᷔ ᷕ ᷖ ᷗ ᷘ ᷙ ᷛ ᷜ ᷝ ᷞ ᷟ ᷠ ᷡ ᷢ ᷣ ᷤ ᷥ ᷦ‘’‛‚“”„‟«»‹›Ꞌ\\\"❛❜❝❞<>@‧¨․꞉:⁚⁝⁞‥…⁖⸪⸬⸫⸭⁛⁘⁙⁏;⦂⁃‐ ‒\\-–⎯—―_⁓⸛⸞⸟ⸯ¬/\\⁄\\⁄|⎜¦‖‗†‡·•⸰°‣⁒%‰‱&⅋§÷\\+±=꞊′″‴⁗‵‶‷‸\\*⁑⁎⁕※⁜⁂!‼¡?¿⸮⁇⁉⁈‽⸘¼½¾²³©®™℠℻℅℁⅍℄¶⁋❡⁌⁍⸖⸗⸚⸓\\(\\)\\[\\]{}⸨⸩❨❩❪❫⸦⸧❬❭❮❯❰❱❴❵❲❳⦗⦘⁅⁆〈〉⏜⏝⏞⏟⸡⸠⸢⸣⸤⸥⎡⎤⎣⎦⎨⎬⌠⌡⎛⎠⎝⎞⁀⁔‿⁐‾⎟⎢⎥⎪ꞁ⎮⎧⎫⎩⎭⎰⎱✈☀☼☁☂☔⚡❄❅❆☃☉☄★☆☽☾⌛⌚☇☈⌂⌁✆☎☏☑✓✔⎷⍻✖✗✘☒✕☓☕♿✌☚☛☜☝☞☟☹☺☻☯⚘☮✝⚰⚱⚠☠☢⚔⚓⎈⚒⚑⚐☡❂⚕⚖⚗✇☣⚙☤⚚⚛⚜☥☦☧☨☩†☪☫☬☭✁✂✃✄✍✎✏✐✑✒✉✙✚✜✛♰♱✞✟✠✡☸✢✣✤✥✦✧✩✪✫✬✭✮✯✰✲✱✳✴✵✶✷✸✹✺✻✼✽✾❀✿❁❃❇❈❉❊❋⁕☘❦❧☙❢❣♀♂⚢⚣⚤⚦⚧⚨⚩☿♁⚯♔♕♖♗♘♙♚♛♜♝♞♟☖☗♠♣♦♥❤❥♡♢♤♧⚀⚁⚂⚃⚄⚅⚇⚆⚈⚉♨♩♪♫♬♭♮♯⌨⏏⎗⎘⎙⎚⌥⎇⌘⌦⌫⌧♲♳♴♵♶♷♸♹♺♻♼♽⁌⁍⎌⌇⌲⍝⍟⍣⍤⍥⍨⍩⎋♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓⏚⏛| | | || | | | | ||](.*)?){0,255}$",
                                                   "^(.*)?\\d(.*)?$",
                                                   true,
                                                   false,
                                                   null,
                                                   password_modal_popup);

    // On every form input event, check if the form is valid.
    const form = document.querySelector('form#admin_login_form');
    const submit_input = form.querySelector("input[type='submit']");
    const fields_validation_instances_list = [email_validation,
                                              password_validation];

    EnableValidation(form, submit_input, fields_validation_instances_list)
});
