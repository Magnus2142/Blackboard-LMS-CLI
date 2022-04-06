image_files = ['jpeg', 'jpg', 'gif', 'svg', 'png', 'tiff', 'tif']
document_files = ['pdf', 'doc', 'docx', 'html', 'htm', 'xls', 'xlsx', 'txt']
video_files = ['mp4', 'avi', 'mov', 'flv', 'avchd']
presentation_files = ['ppt', 'pptx', 'odp', 'key']
audio_files = ['m4a', 'mp3', 'wav']

def get_file_type(fn):
	ft = ''
	ft = ['image_file' for imf in image_files if imf in fn]
	if len(ft) > 0: return ft[0]
	ft = ['document_file' for df in document_files if df in fn]
	if len(ft) > 0: return ft[0]
	ft = ['video_files' for vf in video_files if vf in fn]
	if len(ft) > 0: return ft[0]
	ft = ['presentation_files' for pf in presentation_files if pf in fn]
	if len(ft) > 0: return ft[0]
	ft = ['audio_files' for af in audio_files if af in fn]
	if len(ft) > 0: return ft[0]
	else: 
		print("Could not find any of the files")
		# TODO: maybe throw something
		return 


	

	