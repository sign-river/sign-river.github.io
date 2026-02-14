// ============================================
// 文件管理菜单 - 汉化版
// ============================================

menu(where=sel.count>0 type='file|dir|drive|namespace|back' mode="multiple" title='文件管理' image=\uE253)
{
	// ============================================
	// 复制路径子菜单
	// ============================================
	menu(separator="after" title='复制路径'image=\uE26C)
	{
		// 多选时显示
		item(where=sel.count > 1 title='复制 (@sel.count) 个项目' cmd=command.copy(sel(false, "\n")))

		// 单选时显示完整路径
		item(mode="single" title=@sel.path tip=sel.path cmd=command.copy(sel.path))

		// 快捷方式特殊处理
		item(mode="single" type='file' separator="before" find='.lnk' title='打开文件位置')

		separator

		// 复制父文件夹路径
		item(mode="single" where=@sel.parent.len>3 title=sel.parent cmd=@command.copy(sel.parent))

		separator

		// 复制文件名（含扩展名）
		item(mode="single" type='file|dir|back.dir' title=sel.file.name cmd=command.copy(sel.file.name))

		// 复制文件名（不含扩展名）
		item(mode="single" type='file' where=sel.file.len != sel.file.title.len title=@sel.file.title cmd=command.copy(sel.file.title))

		// 复制扩展名
		item(mode="single" type='file' where=sel.file.ext.len>0 title=sel.file.ext cmd=command.copy(sel.file.ext))
	}

	// ============================================
	// 修改文件扩展名
	// ============================================
	item(mode="single" type="file" title="修改扩展名" image=\uE104 cmd=if(input("修改扩展名", "输入新扩展名"),
		io.rename(sel.path, path.join(sel.dir, sel.file.title + "." + input.result))))

	// ============================================
	// 选择操作子菜单
	// ============================================
	menu(separator="after" image=\uE133 title='选择')
	{
		item(title="全选"  cmd=command.select_all)
		item(title="反选"  cmd=command.invert_selection)
		item(title="取消选择"  cmd=command.select_none)
	}

	// ============================================
	// 获取所有权（需要管理员权限）
	// ============================================
	item(type='file|dir|back.dir|drive' title='获取所有权' image=[\uE1E2,#f00] admin
		cmd args='/K takeown /f "@sel.path" @if(sel.type==1,null,"/r /d y") && icacls "@sel.path" /grant *S-1-5-32-544:F @if(sel.type==1,"/c /l","/t /c /l /q")')

	separator

	// ============================================
	// 显示/隐藏子菜单
	// ============================================
	menu(title="显示/隐藏" image=\uE138)
	{
		item(title="系统文件" cmd='@command.togglehidden')
		item(title="文件扩展名" cmd='@command.toggleext')
	}

	// ============================================
	// 文件属性子菜单
	// ============================================
	menu(type='file|dir|back.dir' mode="single" title='文件属性' image=\uE115)
	{
		$atrr = io.attributes(sel.path)

		// 隐藏属性
		item(title='隐藏' checked=io.attribute.hidden(atrr)
			cmd args='/c ATTRIB @if(io.attribute.hidden(atrr),"-","+")H "@sel.path"' window=hidden)

		// 系统属性
		item(title='系统' checked=io.attribute.system(atrr)
			cmd args='/c ATTRIB @if(io.attribute.system(atrr),"-","+")S "@sel.path"' window=hidden)

		// 只读属性
		item(title='只读' checked=io.attribute.readonly(atrr)
			cmd args='/c ATTRIB @if(io.attribute.readonly(atrr),"-","+")R "@sel.path"' window=hidden)

		// 存档属性
		item(title='存档' checked=io.attribute.archive(atrr)
			cmd args='/c ATTRIB @if(io.attribute.archive(atrr),"-","+")A "@sel.path"' window=hidden)

		separator

		// 显示时间信息（只读）
		item(title="创建时间" keys=io.dt.created(sel.path, 'y/m/d') cmd=io.dt.created(sel.path,2000,1,1) vis=label)
		item(title="修改时间" keys=io.dt.modified(sel.path, 'y/m/d') cmd=io.dt.modified(sel.path,2000,1,1) vis=label)
		item(title="访问时间" keys=io.dt.accessed(sel.path, 'y/m/d') cmd=io.dt.accessed(sel.path,2000,1,1) vis=label)
	}

	// ============================================
	// 注册服务器（仅 DLL/OCX 文件）
	// ============================================
	menu(mode="single" type='file' find='.dll|.ocx' separator="before" title='注册服务器' image=\uE26C)
	{
		item(title='注册' admin cmd='regsvr32.exe' args='@sel.path.quote' invoke="multiple")
		item(title='取消注册' admin cmd='regsvr32.exe' args='/u @sel.path.quote' invoke="multiple")
	}

	// ============================================
	// 新建文件/文件夹（仅在空白处显示）
	// ============================================
	menu(mode="single" type='back' expanded=true)
	{
		// 新建文件夹子菜单
		menu(separator="before" title='新建文件夹' image=\uE0E7)
		{
			item(title='时间戳文件夹' cmd=io.dir.create(sys.datetime("ymdHMSs")))
			item(title='GUID 文件夹' cmd=io.dir.create(str.guid))
		}

		// 新建文件子菜单
		menu(title='新建文件' image=\uE160)
		{
			$dt = sys.datetime("ymdHMSs")

			// 文本文件
			item(title='TXT 文件'  cmd=io.file.create('@(dt).txt', 'Hello World!'))
			item(title='Markdown 文件'  cmd=io.file.create('@(dt).md', '# 标题\n\n这是一个 Markdown 文件。'))

			separator

			// 编程语言文件
			item(title='Python 文件' cmd=io.file.create('@(dt).py', '# Python Script\n\ndef main():\n    print("Hello World!")\n\nif __name__ == "__main__":\n    main()'))
			item(title='JavaScript 文件'  cmd=io.file.create('@(dt).js', '// JavaScript File\n\nconsole.log("Hello World!");'))
			item(title='CSS 文件' cmd=io.file.create('@(dt).css', '/* CSS Stylesheet */\n\nbody {\n    margin: 0;\n    padding: 0;\n}'))

			separator

			// 数据文件
			item(title='JSON 文件'  cmd=io.file.create('@(dt).json', '{\n    "name": "example",\n    "version": "1.0.0"\n}'))
			item(title='XML 文件' cmd=io.file.create('@(dt).xml', '<?xml version="1.0" encoding="UTF-8"?>\n<root>\n    <item>Hello World!</item>\n</root>'))
			item(title='YAML 文件'  cmd=io.file.create('@(dt).yml', '# YAML Configuration\nname: example\nversion: 1.0.0'))
			item(title='CSV 文件'  cmd=io.file.create('@(dt).csv', '姓名，年龄，城市\n张三，25，北京\n李四，30，上海'))

			separator

			// 网页文件
			item(title='HTML 文件'  cmd=io.file.create('@(dt).html', '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <meta charset="UTF-8">\n    <title>标题</title>\n</head>\n<body>\n    <h1>Hello World!</h1>\n</body>\n</html>'))

			separator

			// 配置文件
			item(title='INI 配置文件'  cmd=io.file.create('@(dt).ini', '[Settings]\nkey=value'))
			item(title='ENV 环境变量' cmd=io.file.create('@(dt).env', '# Environment Variables\nAPP_NAME=MyApp\nAPP_ENV=development'))

			separator

			// 批处理和脚本
			item(title='BAT 批处理'  cmd=io.file.create('@(dt).bat', '@echo off\necho Hello World!\npause'))
			item(title='PowerShell 脚本'  cmd=io.file.create('@(dt).ps1', '# PowerShell Script\nWrite-Host "Hello World!"'))
		}
	}

	// ============================================
	// 文件夹选项（非桌面环境显示）
	// ============================================
	item(where=!wnd.is_desktop title='文件夹选项' image=\uE115 cmd=command.folder_options)
}
