import streamlit as st
from utils import TimeHelper
import VideoEditor 

# Cuts array state
if 'cuts' not in st.session_state:
	st.session_state.cuts = [] 

def reset_cuts():
    st.session_state.cuts = []

def generate_video():
    VideoEditor.run(st.session_state.cuts, video_file.name)
    st.balloons()


st.title("Fast Video Trimer")

# Video upload
video_file = st.file_uploader('', type=['mp4'], on_change=reset_cuts)
if (video_file):
    st.video(video_file, "video/mp4")
    

# Sidebar with the video trimming inputs 
if (video_file):
    st.sidebar.header("Adicionar Cortes")
    cuts_form = st.sidebar.form("cuts_form", clear_on_submit=True)
    cut_start_time = cuts_form.text_input("Início do corte", value="00:00:00", placeholder="00:00:00", max_chars=8)
    cut_end_time = cuts_form.text_input("Fim do corte", placeholder="00:01:30", max_chars=8)

    submitted = cuts_form.form_submit_button("Adicionar")

    if (submitted):
        start_format_ok = TimeHelper.check_time_format(cut_start_time)
        end_format_ok = TimeHelper.check_time_format(cut_end_time)
        if (start_format_ok and end_format_ok):
            st.session_state.cuts.append(cut_start_time + ',' + cut_end_time)
        else:
            cuts_form.error("Formato de tempo inválido")
       
    # remove cuts
    st.sidebar.header("Remover Cortes")
    remove_cuts_form = st.sidebar.form("remove_cuts", clear_on_submit=True)
    remove_cuts_options = [''] + [cut.split(',')[0]+' - '+ cut.split(',')[1] for cut in st.session_state.cuts]
    selected_cut = remove_cuts_form.selectbox("Selecionar corte", remove_cuts_options, 0)
    remove_cut_submmited = remove_cuts_form.form_submit_button("Remover")
    if (remove_cut_submmited):
        if (not selected_cut==''):
            cut_to_remove = st.session_state.cuts[remove_cuts_options.index(selected_cut)-1]
            st.session_state.cuts.remove(cut_to_remove)

    # list cuts
    st.sidebar.header("Lista de Cortes")
    expander = st.sidebar.expander("Cortes", True)
    left_column, right_column = expander.columns(2)
    if (len(st.session_state.cuts)):
        left_column.caption("Início do corte")
        right_column.caption("Fim do corte")
    for cut in st.session_state.cuts:
        start_time, end_time = cut.split(',')        
        left_column.text(start_time)
        right_column.text(end_time)

    if (len(st.session_state.cuts)>0):
        st.button("Gerar vídeo", on_click=generate_video)


    
    



