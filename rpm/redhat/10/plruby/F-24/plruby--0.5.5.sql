CREATE FUNCTION plruby_call_handler () RETURNS language_handler
	AS '/usr/lib64/ruby/vendor_ruby/plruby'
        language C;

CREATE OR REPLACE LANGUAGE plruby
	HANDLER  plruby_call_handler;
