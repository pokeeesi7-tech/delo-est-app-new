#!/usr/bin/env python3
"""Apply Studio v5 design tokens and a native-first home page to Flutter source."""
from pathlib import Path
import re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
def read(name):
 p=root/name
 if not p.exists():raise SystemExit(f'Missing {p}')
 return p,p.read_text(encoding='utf-8')
def write(p,s):p.write_text(s,encoding='utf-8')
p,s=read('theme.dart')
repls={'Color(0xFFFDF8F3)':'Color(0xFFF4F7FC)','Color(0xFFF7EFE6)':'Color(0xFFEAF0F8)','Color(0xFF1B1530)':'Color(0xFF152039)','Color(0xFF6B6480)':'Color(0xFF65738B)','Color(0xFFEADFD3)':'Color(0xFFDCE4F0)','Color(0xFFFF5A36)':'Color(0xFF405CF5)','Color(0xFFFF9F1C)':'Color(0xFF19B99A)','Color(0xFF12A150)':'Color(0xFF0C9B72)','Color(0xFFC0262D)':'Color(0xFFD74454)','Color(0xFF0A0E1F)':'Color(0xFF0A1120)','Color(0xFF0E1429)':'Color(0xFF111D30)','Color(0xFF121833)':'Color(0xFF142138)','Color(0xFFEEF1FF)':'Color(0xFFF2F6FC)','Color(0xFF9AA3C7)':'Color(0xFFA1B0C6)','Color(0xFF232B52)':'Color(0xFF283850)','Color(0xFF7C5CFF)':'Color(0xFF8EA2FF)','Color(0xFF22D3EE)':'Color(0xFF4AD8BD)','Color(0xFF4ADE80)':'Color(0xFF4BE0B2)','Color(0xFFFF7B84)':'Color(0xFFFF8491)'}
for old,new in repls.items():s=s.replace(old,new)
if 'elevatedButtonTheme:' not in s:s=s.replace('    outlinedButtonTheme: OutlinedButtonThemeData(\n','''    elevatedButtonTheme: ElevatedButtonThemeData(style: ElevatedButton.styleFrom(foregroundColor: Colors.white, backgroundColor: p.ac, elevation: 0, minimumSize: const Size(0, 46), padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12), textStyle: const TextStyle(fontWeight: FontWeight.w800), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)))),\n    outlinedButtonTheme: OutlinedButtonThemeData(\n''',1)
write(p,s)
p,s=read('landing.dart');a=s.find('  @override\n  Widget build(BuildContext context) {');b=s.find('\n  Widget _topBar(Pal p)',a)
if a<0 or b<0:raise SystemExit('Could not locate landing build/top bar')
build='''  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(listenable: S.i, builder: (context, _) {
      final p=pal(context); final recent=List<Ad>.of(S.i.ads)..sort((a,b)=>b.ts.compareTo(a.ts));
      return Scaffold(body: SafeArea(bottom:false,child:RefreshIndicator(color:p.ac,onRefresh:() async {await Future.wait([S.i.loadAds(),_loadSite()]);},
        child:CustomScrollView(physics:const AlwaysScrollableScrollPhysics(),slivers:[
          SliverToBoxAdapter(child:_topBar(p)),
          SliverToBoxAdapter(child:_hero(p)),
          SliverToBoxAdapter(child:_sectionTitle(p,'Категории','Выберите направление и найдите подходящие задания.')),
          SliverToBoxAdapter(child:_categories(p)),
          SliverToBoxAdapter(child:_sectionTitle(p,'Свежие объявления','Новые предложения и разовые заказы.',action:'Все объявления',onAction:()=>S.i.goTab(1))),
          if(S.i.loading&&recent.isEmpty) SliverPadding(padding:const EdgeInsets.symmetric(horizontal:16),sliver:SliverList(delegate:SliverChildBuilderDelegate((context,i)=>Container(height:118,margin:const EdgeInsets.only(bottom:10),decoration:BoxDecoration(color:p.card,borderRadius:BorderRadius.circular(18),border:Border.all(color:p.bd)),padding:const EdgeInsets.all(14),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Container(width:90,height:10,decoration:BoxDecoration(color:p.bg2,borderRadius:BorderRadius.circular(20))),const SizedBox(height:16),Container(width:double.infinity,height:13,decoration:BoxDecoration(color:p.bg2,borderRadius:BorderRadius.circular(20))),const SizedBox(height:10),Container(width:155,height:10,decoration:BoxDecoration(color:p.bg2,borderRadius:BorderRadius.circular(20)))]),),childCount:3)))
          else if(recent.isEmpty) SliverToBoxAdapter(child:_emptyAds(p))
          else SliverPadding(padding:const EdgeInsets.fromLTRB(16,0,16,8),sliver:SliverList(delegate:SliverChildBuilderDelegate((context,i)=>AdCard(ad:recent[i],onTap:()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>AdPage(ad:recent[i])))),childCount:recent.length>6?6:recent.length))),
          SliverToBoxAdapter(child:Padding(padding:const EdgeInsets.fromLTRB(16,6,16,28),child:OutlinedButton.icon(onPressed:()=>S.i.goTab(1),icon:const Icon(Icons.tune_rounded),label:const Text('Подобрать по фильтрам'),style:OutlinedButton.styleFrom(minimumSize:const Size.fromHeight(48),foregroundColor:p.ac,side:BorderSide(color:p.ac.withOpacity(.35)))))),
        ]))));
    });
  }
'''
s=s[:a]+build+s[b:]
a=s.find('  Widget _topBar(Pal p)');b=s.find('\n  Widget _hero(Pal p)',a)
top='''  Widget _topBar(Pal p) {
    final mode=S.i.themeMode;final icon=mode==ThemeMode.system?Icons.brightness_auto_rounded:mode==ThemeMode.dark?Icons.dark_mode_rounded:Icons.light_mode_rounded;
    final label=mode==ThemeMode.system?'Системная тема':mode==ThemeMode.dark?'Тёмная тема':'Светлая тема';
    return Padding(padding:const EdgeInsets.fromLTRB(16,10,12,8),child:Row(children:[
      const Logo(size:38),const SizedBox(width:10),
      Column(crossAxisAlignment:CrossAxisAlignment.start,children:[Text('ДелоЕсть',style:TextStyle(fontSize:20,height:1.15,letterSpacing:-.7,fontWeight:FontWeight.w900,color:p.tx)),Text('Работа рядом',style:TextStyle(fontSize:11.5,color:p.mu,fontWeight:FontWeight.w600))]),
      const Spacer(),
      IconButton(tooltip:'$label · нажмите, чтобы сменить',onPressed:()=>S.i.setTheme(mode==ThemeMode.system?ThemeMode.light:mode==ThemeMode.light?ThemeMode.dark:ThemeMode.system),icon:Icon(icon,color:p.mu),style:IconButton.styleFrom(backgroundColor:p.card,side:BorderSide(color:p.bd))),
      if(S.i.logged)...[const SizedBox(width:6),IconButton(tooltip:'Сообщения',onPressed:()=>S.i.goTab(4),icon:Stack(clipBehavior:Clip.none,children:[Icon(Icons.chat_bubble_outline_rounded,color:p.tx),if(S.i.unread>0)Positioned(right:-7,top:-6,child:Container(width:9,height:9,decoration:BoxDecoration(color:p.ac2,shape:BoxShape.circle,border:Border.all(color:p.card,width:1.5))))]),style:IconButton.styleFrom(backgroundColor:p.card,side:BorderSide(color:p.bd)))]
    ]));
  }
'''
if a<0 or b<0:raise SystemExit('Could not locate topbar boundary')
s=s[:a]+top+s[b:]
pat=r"        const SizedBox\(height: 13\),\s*SingleChildScrollView\(\s*scrollDirection: Axis\.horizontal,.*?\n        \),\n      \]\),"
s=re.sub(pat,'      ]),',s,count=1,flags=re.S)
s=s.replace('''        color: p.card,
        borderRadius: BorderRadius.circular(26),
        border: Border.all(color: p.bd),
        gradient: LinearGradient(''','''        borderRadius: BorderRadius.circular(22),
        border: Border.all(color: p.bd),
        gradient: LinearGradient(''',1)
s=s.replace('borderRadius: BorderRadius.circular(26),','borderRadius: BorderRadius.circular(22),',1)
write(p,s)
p,s=read('settings.dart')
s=s.replace("_iconChoice(p, 'orange', 'Апельсин', 'assets/icon_orange.png', const Color(0xFFFF6A2A))","_iconChoice(p, 'orange', 'Кобальт', 'assets/icon_orange.png', const Color(0xFF405CF5))")
s=s.replace("_iconChoice(p, 'purple', 'Фиолет', 'assets/icon_purple.png', const Color(0xFF7C5CFF))","_iconChoice(p, 'purple', 'Мята', 'assets/icon_purple.png', const Color(0xFF19B99A))")
write(p,s)
p,s=read('pubspec.yaml');s=s.replace('adaptive_icon_background: "#ff5a36"','adaptive_icon_background: "#405CF5"');write(p,s)
print(f'Applied Studio v5 native UI under {root}')
