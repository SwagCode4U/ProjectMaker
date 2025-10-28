# Thin adapter over existing templates so framework modules can import them as T
from app.services.templates import BackendTemplates as BT, FrontendTemplates as FT

# Helpers for safe getattr with defaults
_def = lambda x='': (lambda *args, **kwargs: x)

# Backend
fastapi_root_app = getattr(BT, 'fastapi_root_app', _def())
fastapi_main = getattr(BT, 'fastapi_main', _def())
fastapi_database = getattr(BT, 'fastapi_database', _def())
fastapi_models = getattr(BT, 'fastapi_models', _def())
fastapi_schemas = getattr(BT, 'fastapi_schemas', _def())
fastapi_crud = getattr(BT, 'fastapi_crud', _def())
fastapi_routes = getattr(BT, 'fastapi_routes', _def())
fastapi_requirements = getattr(BT, 'fastapi_requirements', _def(''))

# Django
django_manage = getattr(BT, 'django_manage', _def(''))
django_settings = getattr(BT, 'django_settings', _def(''))
django_urls = getattr(BT, 'django_urls', _def(''))
django_wsgi = getattr(BT, 'django_wsgi', _def(''))
django_requirements = getattr(BT, 'django_requirements', _def(''))

env_example = getattr(BT, 'env_example', _def(''))

# Flask
flask_app = getattr(BT, 'flask_app', _def(''))
flask_config = getattr(BT, 'flask_config', _def(''))
flask_models = getattr(BT, 'flask_models', _def(''))
flask_routes = getattr(BT, 'flask_routes', _def(''))
flask_requirements = getattr(BT, 'flask_requirements', _def(''))

express_package_json = getattr(BT, 'express_package_json', _def('{}'))
express_app_js = getattr(BT, 'express_app_js', _def("import express from 'express'\nexport default express()\n"))
express_server_js = getattr(BT, 'express_server_js', _def("import app from './app.js'\napp.listen(process.env.PORT||5177)\n"))
express_routes_index_js = getattr(BT, 'express_routes_index_js', _def("""import { Router } from 'express'
import { home } from '../controllers/homeController.js'

const router = Router()
router.get('/', home)
export default router
"""))
express_home_controller_js = getattr(BT, 'express_home_controller_js', _def("export const home=(req,res)=>res.json({message:'Welcome to Express Boilerplate!'})\n"))
express_error_handler_js = getattr(BT, 'express_error_handler_js', _def("export const errorHandler=(err,req,res,next)=>{console.error(err.stack);res.status(500).json({error:'Something went wrong!'})}\n"))
express_logger_js = getattr(BT, 'express_logger_js', _def("export const log=(msg)=>console.log(`[LOG]: ${msg}`)\n"))
express_env_example = getattr(BT, 'express_env_example', _def("PORT=5177\n"))
express_readme = getattr(BT, 'express_readme', _def("# Express Boilerplate\n\nRun: npm i && npm run dev\n"))

# Frontend
react_package_json = getattr(FT, 'react_package_json', _def('{}'))
react_index_html = getattr(FT, 'react_index_html', _def('<!DOCTYPE html>'))
react_app = getattr(FT, 'react_app', _def(''))
react_main = getattr(FT, 'react_main', _def(''))
react_css = getattr(FT, 'react_css', _def(''))
react_navbar = getattr(FT, 'react_navbar', _def(''))
react_hero = getattr(FT, 'react_hero', _def(''))
react_use_lenis = getattr(FT, 'react_use_lenis', _def(''))
react_theme = getattr(FT, 'react_theme', _def(''))
react_footer = getattr(FT, 'react_footer', _def(''))
react_readme = getattr(FT, 'react_readme', _def(''))

svelte_package_json = getattr(FT, 'svelte_package_json', _def('{}'))
svelte_vite_config = getattr(FT, 'svelte_vite_config', _def(''))
svelte_index_html = getattr(FT, 'svelte_index_html', _def('<!DOCTYPE html>'))
svelte_app = getattr(FT, 'svelte_app', _def(''))
svelte_app_css = getattr(FT, 'svelte_app_css', _def(''))
svelte_lib_api_js = getattr(FT, 'svelte_lib_api_js', _def(''))
svelte_lib_utils_js = getattr(FT, 'svelte_lib_utils_js', _def(''))
svelte_home = getattr(FT, 'svelte_home', _def(''))
svelte_explorer = getattr(FT, 'svelte_explorer', _def(''))
svelte_create_file = getattr(FT, 'svelte_create_file', _def(''))
svelte_db_designer = getattr(FT, 'svelte_db_designer', _def(''))

tailwind_config = getattr(FT, 'tailwind_config', _def(''))
postcss_config = getattr(FT, 'postcss_config', _def(''))

nextjs_package_json = getattr(FT, 'nextjs_package_json', _def('{}'))
nextjs_config = getattr(FT, 'nextjs_config', _def(''))
nextjs_layout = getattr(FT, 'nextjs_layout', _def(''))
nextjs_page = getattr(FT, 'nextjs_page', _def(''))

# Angular
angular_package_json = getattr(FT, 'angular_package_json', _def('{}'))
angular_json = getattr(FT, 'angular_json', _def('{}'))
angular_index_html = getattr(FT, 'angular_index_html', _def('<!DOCTYPE html>'))
angular_main = getattr(FT, 'angular_main', _def(''))
angular_component = getattr(FT, 'angular_component', _def(''))
angular_app_module = getattr(FT, 'angular_app_module', _def(''))
angular_app_routing_module = getattr(FT, 'angular_app_routing_module', _def(''))
angular_header_component_ts = getattr(FT, 'angular_header_component_ts', _def(''))
angular_header_component_html = getattr(FT, 'angular_header_component_html', _def(''))
angular_footer_component_ts = getattr(FT, 'angular_footer_component_ts', _def(''))
angular_footer_component_html = getattr(FT, 'angular_footer_component_html', _def(''))
angular_home_component_ts = getattr(FT, 'angular_home_component_ts', _def(''))
angular_home_component_html = getattr(FT, 'angular_home_component_html', _def(''))
angular_about_component_ts = getattr(FT, 'angular_about_component_ts', _def(''))
angular_about_component_html = getattr(FT, 'angular_about_component_html', _def(''))
