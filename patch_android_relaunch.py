#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
def rw(name,fn):
 p=root/name
 if not p.exists(): raise SystemExit(f'Missing {p}')
 s=p.read_text(encoding='utf-8');p.write_text(fn(s),encoding='utf-8')
colors={
'Color(0xFFFDF8F3)':'Color(0xFFF4F5EF)','Color(0xFFF7EFE6)':'Color(0xFFE9ECE2)','Color(0xFF1B1530)':'Color(0xFF17251F)','Color(0xFF6B6480)':'Color(0xFF68766C)','Color(0xFFEADFD3)':'Color(0xFFDCE2D6)','Color(0xFFFF5A36)':'Color(0xFFB6E64C)','Color(0xFFFF9F1C)':'Color(0xFF244F3D)','Color(0xFF12A150)':'Color(0xFF21835B)','Color(0xFFC0262D)':'Color(0xFFD44848)','Color(0xFF0A0E1F)':'Color(0xFF101914)','Color(0xFF0E1429)':'Color(0xFF19251D)','Color(0xFF121833)':'Color(0xFF202D24)','Color(0xFFEEF1FF)':'Color(0xFFF1F4EB)','Color(0xFF9AA3C7)':'Color(0xFFA2B0A2)','Color(0xFF232B52)':'Color(0xFF344338)','Color(0xFF7C5CFF)':'Color(0xFFC3F36A)','Color(0xFF22D3EE)':'Color(0xFFB6E64C)','Color(0xFF4ADE80)':'Color(0xFF73D5A2)','Color(0xFFFF7B84)':'Color(0xFFFF8888)'}
for p in root.glob('*.dart'):
 s=p.read_text(encoding='utf-8')
 for a,b in colors.items():s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
def theme(s):
 if 'DELO_FIELD_NOTES_THEME' in s:return s
 return s.replace('    visualDensity: VisualDensity.standard,','''    visualDensity: VisualDensity.standard,
    // DELO_FIELD_NOTES_THEME: consistent native controls.
    listTileTheme: ListTileThemeData(iconColor: p.mu, textColor: p.tx, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
    elevatedButtonTheme: ElevatedButtonThemeData(style: ElevatedButton.styleFrom(foregroundColor: p.tx, backgroundColor: p.ac, elevation: 0, minimumSize: const Size(0, 48), padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 13), textStyle: const TextStyle(fontWeight: FontWeight.w800), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)))),
    inputDecorationTheme: InputDecorationTheme(filled: true, fillColor: p.card, hintStyle: TextStyle(color: p.mu.withOpacity(.8)), contentPadding: const EdgeInsets.symmetric(horizontal: 15, vertical: 15), border: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: BorderSide(color: p.bd)), enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: BorderSide(color: p.bd)), focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: BorderSide(color: p.ac, width: 1.5))),
''',1)
rw('theme.dart',theme)
def landing(s):
 if 'DELO_FIELD_NOTES_HOME' in s:return s
 a=s.find('  @override\n  Widget build(BuildContext context) {');b=s.find('\n  Widget _topBar(Pal p)',a)
 if a<0 or b<0:raise SystemExit('landing build boundaries missing')
 build='''  // DELO_FIELD_NOTES_HOME
  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(listenable:S.i,builder:(context,_) {
      final p=pal(context);final ads=List<Ad>.of(S.i.ads)..sort((a,b)=>b.ts.compareTo(a.ts));final wide=MediaQuery.sizeOf(context).width>=700;
      return Scaffold(body:SafeArea(bottom:false,child:RefreshIndicator(color:p.ac,onRefresh:() async {await Future.wait([S.i.loadAds(),_loadSite()]);},child:CustomScrollView(physics:const AlwaysScrollableScrollPhysics(),slivers:[
        SliverToBoxAdapter(child:_topBar(p)),SliverToBoxAdapter(child:_hero(p)),
        SliverToBoxAdapter(child:_sectionTitle(p,'Найдите своё направление','Выберите категорию и смотрите подходящие предложения.')),
        SliverToBoxAdapter(child:_categories(p)),
        SliverToBoxAdapter(child:_sectionTitle(p,'Новые предложения','Свежие задания от людей и компаний.',action:'Вся лента',onAction:()=>S.i.goTab(1))),
        if(S.i.loading&&ads.isEmpty) SliverPadding(padding:const EdgeInsets.symmetric(horizontal:16),sliver:SliverList(delegate:SliverChildBuilderDelegate((context,i)=>Container(height:105,margin:const EdgeInsets.only(bottom:10),decoration:BoxDecoration(color:p.card,borderRadius:BorderRadius.circular(18),border:Border.all(color:p.bd)),padding:const EdgeInsets.all(15),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Container(width:90,height:9,decoration:BoxDecoration(color:p.bg2,borderRadius:BorderRadius.circular(20))),const SizedBox(height:15),Container(width:double.infinity,height:12,decoration:BoxDecoration(color:p.bg2,borderRadius:BorderRadius.circular(20))),const SizedBox(height:9),Container(width:145,height:9,decoration:BoxDecoration(color:p.bg2,borderRadius:BorderRadius.circular(20)))])),childCount:3)))
        else if(ads.isEmpty) SliverToBoxAdapter(child:_emptyAds(p))
        else SliverPadding(padding:const EdgeInsets.fromLTRB(16,0,16,8),sliver:SliverGrid(delegate:SliverChildBuilderDelegate((context,i)=>AdCard(ad:ads[i],onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>AdPage(ad:ads[i]))),showFav:true),childCount:ads.length>(S.i.logged?8:6)?(S.i.logged?8:6):ads.length),gridDelegate:SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount:wide?2:1,mainAxisExtent:wide?250:195,crossAxisSpacing:12,mainAxisSpacing:10))),
        SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.fromLTRB(16,8,16,30),child:OutlinedButton.icon(onPressed:()=>S.i.goTab(1),icon:const Icon(Icons.tune_rounded),label:const Text('Настроить поиск'),style:OutlinedButton.styleFrom(minimumSize:const Size.fromHeight(50),foregroundColor:p.tx,side:BorderSide(color:p.bd))))),
      ]))));
    });
  }
'''
 return s[:a]+build+s[b:]
rw('landing.dart',landing)
def topbar(s):
 a=s.find('  Widget _topBar(Pal p)');b=s.find('\n  Widget _hero(Pal p)',a)
 if a<0 or b<0:raise SystemExit('top bar boundaries missing')
 top='''  Widget _topBar(Pal p) {
    final mode=S.i.themeMode;final icon=mode==ThemeMode.system?Icons.brightness_auto_rounded:mode==ThemeMode.dark?Icons.dark_mode_rounded:Icons.light_mode_rounded;
    return Padding(padding:const EdgeInsets.fromLTRB(16,10,12,8),child:Row(children:[
      Container(width:42,height:42,decoration:BoxDecoration(color:p.ac,borderRadius:BorderRadius.circular(14)),child:const Icon(Icons.check_rounded,color:Color(0xFF17251F),size:26)),
      const SizedBox(width:10),Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text('ДелоЕсть',style:TextStyle(fontSize:20,height:1.1,letterSpacing:-.8,fontWeight:FontWeight.w900,color:p.tx)),Text('Найди своё дело',style:TextStyle(fontSize:11.5,color:p.mu,fontWeight:FontWeight.w600))]),
      const Spacer(),IconButton(tooltip:'Сменить тему',onPressed:()=>S.i.setTheme(mode==ThemeMode.system?ThemeMode.light:mode==ThemeMode.light?ThemeMode.dark:ThemeMode.system),icon:Icon(icon,color:p.tx),style:IconButton.styleFrom(backgroundColor:p.card,side:BorderSide(color:p.bd))),
      if(S.i.logged)...[const SizedBox(width:5),IconButton(tooltip:'Сообщения',onPressed:()=>S.i.goTab(4),icon:Stack(clipBehavior:Clip.none,children:[Icon(Icons.chat_bubble_outline_rounded,color:p.tx),if(S.i.unread>0)Positioned(right:-7,top:-6,child:Container(width:9,height:9,decoration:BoxDecoration(color:p.ac,shape:BoxShape.circle,border:Border.all(color:p.card,width:1.5))))]),style:IconButton.styleFrom(backgroundColor:p.card,side:BorderSide(color:p.bd))]
    ]));
  }
'''
 return s[:a]+top+s[b:]
rw('landing.dart',lambda s:topbar(s))
def hero(s):
 a=s.find('  Widget _hero(Pal p)');b=s.find('\n  Widget _cityAutocomplete(Pal p)',a)
 if a<0 or b<0:raise SystemExit('hero boundaries missing')
 h='''  Widget _hero(Pal p) {
    final logged=S.i.logged;const ink=Color(0xFF17251F);const forest=Color(0xFF244F3D);
    return Container(margin:const EdgeInsets.fromLTRB(14,8,14,10),padding:const EdgeInsets.fromLTRB(20,24,20,18),decoration:BoxDecoration(color:p.ac,borderRadius:BorderRadius.circular(25)),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
      Row(mainAxisSize:MainAxisSize.min,children:[Container(width:7,height:7,decoration:const BoxDecoration(color:forest,shape:BoxShape.circle)),const SizedBox(width:8),Text(logged?'С ВОЗВРАЩЕНИЕМ':'РАБОТА И ЗАКАЗЫ РЯДОМ',style:const TextStyle(color:forest,fontSize:10,letterSpacing:1.1,fontWeight:FontWeight.w900))]),
      const SizedBox(height:17),Text(logged?(S.i.name.trim().isEmpty?'Продолжим?':'Снова в деле, ${S.i.name.trim()}'):'Найди своё\\nдело.',style:const TextStyle(color:ink,fontSize:36,height:1.02,letterSpacing:-1.4,fontWeight:FontWeight.w900)),
      const SizedBox(height:10),Text(logged?'Новые задания и люди — здесь.':'Подработка на сегодня. Исполнитель на сейчас. Без лишних шагов.',style:TextStyle(color:forest.withOpacity(.9),fontSize:13.5,height:1.45,fontWeight:FontWeight.w600)),
      const SizedBox(height:20),Container(padding:const EdgeInsets.all(4),decoration:BoxDecoration(color:forest.withOpacity(.10),borderRadius:BorderRadius.circular(14)),child:Row(children:[Expanded(child:_modeButton(p,'Ищу подработку',0)),Expanded(child:_modeButton(p,'Ищу исполнителя',1))])),
      const SizedBox(height:10),Container(padding:const EdgeInsets.symmetric(horizontal:13,vertical:2),decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(15)),child:TextField(controller:_q,textInputAction:TextInputAction.search,onSubmitted:(_)=>_search(),style:const TextStyle(color:ink,fontSize:14),decoration:const InputDecoration(border:InputBorder.none,enabledBorder:InputBorder.none,focusedBorder:InputBorder.none,hintText:'Что нужно сделать?',prefixIcon:Icon(Icons.search_rounded,color:forest)))),
      const SizedBox(height:9),Container(padding:const EdgeInsets.symmetric(horizontal:13,vertical:2),decoration:BoxDecoration(color:Colors.white,borderRadius:BorderRadius.circular(15)),child:_cityAutocomplete(p)),
      const SizedBox(height:12),SizedBox(width:double.infinity,child:ElevatedButton.icon(onPressed:_search,icon:const Icon(Icons.arrow_forward_rounded),label:const Text('Найти объявления'),style:ElevatedButton.styleFrom(backgroundColor:ink,foregroundColor:const Color(0xFFF4F5EF),minimumSize:const Size.fromHeight(50),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(13)))))
    ]));
  }
'''
 return s[:a]+h+s[b:]
rw('landing.dart',hero)
def widgets(s):
 s=s.replace('child: Icon(Icons.check_rounded, color: Colors.white, size: size * .68),','child: Icon(Icons.check_rounded, color: p.tx, size: size * .68),')
 s=s.replace('CircularProgressIndicator(strokeWidth: 2.4, color: Colors.white)','CircularProgressIndicator(strokeWidth: 2.4, color: p.tx)')
 s=s.replace('Icon(icon, color: Colors.white, size: 21)','Icon(icon, color: p.tx, size: 21)')
 s=s.replace('Text(text, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 16))','Text(text, style: TextStyle(color: p.tx, fontWeight: FontWeight.w800, fontSize: 16))')
 return s
rw('widgets.dart',widgets)
rw('pubspec.yaml',lambda s:s.replace('adaptive_icon_background: "#ff5a36"','adaptive_icon_background: "#b6e64c"').replace('adaptive_icon_background: "#FF5A36"','adaptive_icon_background: "#b6e64c"'))
print('Applied Field Notes native redesign')
