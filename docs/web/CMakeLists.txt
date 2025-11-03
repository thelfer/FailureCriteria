pandoc_html(index "--toc" "--number-sections" "--toc-depth=2")
pandoc_html(install "--toc")
pandoc_html(contributing "--toc")
pandoc_html(contributors)

if(MFM_APPEND_SUFFIX)
  install(DIRECTORY js css img
    DESTINATION share/doc/mfm-${MFM_SUFFIX}/web
    COMPONENT website)
else(MFM_APPEND_SUFFIX)
  install(DIRECTORY js css img
    DESTINATION share/doc/mfm/web
    COMPONENT website)
endif(MFM_APPEND_SUFFIX)
