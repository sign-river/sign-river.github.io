menu(type='*' where=window.is_taskbar||sel.count mode=mode.multiple title=title.go_to sep=sep.both image=\uE14A)
{
	menu(title='文件夹' image=\uE1F4)
	{
		item(title='Windows'  cmd=sys.dir)
		item(title='System'  cmd=sys.bin)
		item(title='Program Files'  cmd=sys.prog)
		item(title='Program Files x86'  cmd=sys.prog32)
		item(title='ProgramData'  cmd=sys.programdata)
		item(title='Applications' cmd='shell:appsfolder')
		item(title='Users'  cmd=sys.users)
		separator
		//item(title='@user.name@@@sys.name' vis=label)
		item(title='桌面' cmd=user.desktop)
		item(title='下载'  cmd=user.downloads)
		item(title='图片'  cmd=user.pictures)
		item(title='文档'  cmd=user.documents)
		item(title='开始菜单'  cmd=user.startmenu)
		item(title='Profile'  cmd=user.dir)
		item(title='AppData'  cmd=user.appdata)
		item(title='Temp' cmd=user.temp)
	}
	item(title=title.control_panel image=\uE0F3 cmd='shell:::{5399E694-6CE5-4D6C-8FCE-1D8870FDCBA0}')
	item(title='所有控制面板项' image=\uE0F3 cmd='shell:::{ED7BA470-8E54-465E-825C-99712043E01C}')
	item(title=title.run image=\uE14B cmd='shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}')
	menu(where=sys.ver.major >= 10 title=title.settings sep=sep.before image=\uE0F3)
	{
		// https://docs.microsoft.com/en-us/windows/uwp/launch-resume/launch-settings-app
		item(title='系统'  cmd='ms-settings:')
		item(title='关于'  cmd='ms-settings:about')
		item(title='你的信息'  cmd='ms-settings:yourinfo')
		item(title='系统信息'  cmd-line='/K systeminfo')
		item(title='搜索' cmd='search-ms:' )
		item(title='USB'  cmd='ms-settings:usb')
		item(title='Windows 更新'  cmd='ms-settings:windowsupdate')
		item(title='Windows 安全中心'  cmd='ms-settings:windowsdefender')
		menu(title='应用' )
		{
			item(title='应用和功能'  cmd='ms-settings:appsfeatures')
			item(title='默认应用'  cmd='ms-settings:defaultapps')
			item(title='可选功能'  cmd='ms-settings:optionalfeatures')
			item(title='启动'  cmd='ms-settings:startupapps')
		}
		menu(title='个性化' )
		{
			item(title='个性化'  cmd='ms-settings:personalization')
			item(title='锁屏界面'  cmd='ms-settings:lockscreen')
			item(title='背景'  cmd='ms-settings:personalization-background')
			item(title='颜色'  cmd='ms-settings:colors')
			item(title='主题'  cmd='ms-settings:themes')
			item(title='开始'  cmd='ms-settings:personalization-start')
			item(title='任务栏'  cmd='ms-settings:taskbar')
		}
		menu(title='网络' )
		{
			item(title='状态'  cmd='ms-settings:network-status')
			item(title='以太网'  cmd='ms-settings:network-ethernet')
			item(title='连接'  cmd='shell:::{7007ACC7-3202-11D1-AAD2-00805FC1270E}')
		}
	}
}